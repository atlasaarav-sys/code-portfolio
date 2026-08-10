#pragma once

#include <memory>
#include <sstream>
#include <string>
#include <variant>
#include <vector>

class JsonValue;

using JsonArray = std::vector<JsonValue>;
using JsonObject = std::vector<std::pair<std::string, JsonValue>>; // insertion-ordered

class JsonValue {
public:
    using Storage = std::variant<std::nullptr_t, bool, double, std::string, JsonArray, JsonObject>;

    JsonValue() : data_(nullptr) {}
    JsonValue(std::nullptr_t) : data_(nullptr) {}
    JsonValue(bool b) : data_(b) {}
    JsonValue(double d) : data_(d) {}
    JsonValue(std::string s) : data_(std::move(s)) {}
    JsonValue(JsonArray a) : data_(std::move(a)) {}
    JsonValue(JsonObject o) : data_(std::move(o)) {}

    bool is_null() const { return std::holds_alternative<std::nullptr_t>(data_); }
    bool is_bool() const { return std::holds_alternative<bool>(data_); }
    bool is_number() const { return std::holds_alternative<double>(data_); }
    bool is_string() const { return std::holds_alternative<std::string>(data_); }
    bool is_array() const { return std::holds_alternative<JsonArray>(data_); }
    bool is_object() const { return std::holds_alternative<JsonObject>(data_); }

    bool as_bool() const { return std::get<bool>(data_); }
    double as_number() const { return std::get<double>(data_); }
    const std::string &as_string() const { return std::get<std::string>(data_); }
    const JsonArray &as_array() const { return std::get<JsonArray>(data_); }
    const JsonObject &as_object() const { return std::get<JsonObject>(data_); }

    const JsonValue *find(const std::string &key) const {
        if (!is_object()) return nullptr;
        for (const auto &[k, v] : as_object()) {
            if (k == key) return &v;
        }
        return nullptr;
    }

    std::string dump() const {
        std::ostringstream out;
        dump_to(out);
        return out.str();
    }

private:
    void dump_to(std::ostringstream &out) const {
        std::visit([&](auto &&value) { dump_value(out, value); }, data_);
    }

    static void dump_value(std::ostringstream &out, std::nullptr_t) { out << "null"; }
    static void dump_value(std::ostringstream &out, bool b) { out << (b ? "true" : "false"); }

    static void dump_value(std::ostringstream &out, double d) {
        if (d == static_cast<long long>(d)) {
            out << static_cast<long long>(d);
        } else {
            out << d;
        }
    }

    static void dump_value(std::ostringstream &out, const std::string &s) {
        out << '"';
        for (char c : s) {
            switch (c) {
                case '"': out << "\\\""; break;
                case '\\': out << "\\\\"; break;
                case '\n': out << "\\n"; break;
                case '\t': out << "\\t"; break;
                default: out << c;
            }
        }
        out << '"';
    }

    void dump_value(std::ostringstream &out, const JsonArray &arr) const {
        out << '[';
        for (size_t i = 0; i < arr.size(); i++) {
            if (i > 0) out << ',';
            arr[i].dump_to(out);
        }
        out << ']';
    }

    void dump_value(std::ostringstream &out, const JsonObject &obj) const {
        out << '{';
        for (size_t i = 0; i < obj.size(); i++) {
            if (i > 0) out << ',';
            dump_value(out, obj[i].first);
            out << ':';
            obj[i].second.dump_to(out);
        }
        out << '}';
    }

    Storage data_;
};
