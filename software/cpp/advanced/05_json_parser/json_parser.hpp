#pragma once

#include <cctype>
#include <cstdlib>
#include <stdexcept>
#include <string>

#include "json_value.hpp"

class JsonParseError : public std::runtime_error {
public:
    explicit JsonParseError(const std::string &msg) : std::runtime_error(msg) {}
};

class JsonParser {
public:
    explicit JsonParser(const std::string &text) : text_(text), pos_(0) {}

    JsonValue parse() {
        skip_whitespace();
        JsonValue value = parse_value();
        skip_whitespace();
        if (pos_ != text_.size()) {
            throw JsonParseError("trailing characters after JSON value at position " + std::to_string(pos_));
        }
        return value;
    }

private:
    const std::string &text_;
    size_t pos_;

    char peek() {
        if (pos_ >= text_.size()) throw JsonParseError("unexpected end of input");
        return text_[pos_];
    }

    char advance() { return text_[pos_++]; }

    void expect(char c) {
        if (pos_ >= text_.size() || text_[pos_] != c) {
            throw JsonParseError(std::string("expected '") + c + "' at position " + std::to_string(pos_));
        }
        pos_++;
    }

    void skip_whitespace() {
        while (pos_ < text_.size() && std::isspace(static_cast<unsigned char>(text_[pos_]))) {
            pos_++;
        }
    }

    JsonValue parse_value() {
        skip_whitespace();
        char c = peek();
        if (c == '{') return parse_object();
        if (c == '[') return parse_array();
        if (c == '"') return JsonValue(parse_string());
        if (c == 't' || c == 'f') return parse_bool();
        if (c == 'n') return parse_null();
        return parse_number();
    }

    JsonValue parse_object() {
        expect('{');
        JsonObject obj;
        skip_whitespace();
        if (peek() == '}') {
            advance();
            return JsonValue(std::move(obj));
        }
        while (true) {
            skip_whitespace();
            std::string key = parse_string();
            skip_whitespace();
            expect(':');
            JsonValue value = parse_value();
            obj.emplace_back(std::move(key), std::move(value));
            skip_whitespace();
            char c = advance();
            if (c == '}') break;
            if (c != ',') throw JsonParseError("expected ',' or '}' in object");
        }
        return JsonValue(std::move(obj));
    }

    JsonValue parse_array() {
        expect('[');
        JsonArray arr;
        skip_whitespace();
        if (peek() == ']') {
            advance();
            return JsonValue(std::move(arr));
        }
        while (true) {
            arr.push_back(parse_value());
            skip_whitespace();
            char c = advance();
            if (c == ']') break;
            if (c != ',') throw JsonParseError("expected ',' or ']' in array");
        }
        return JsonValue(std::move(arr));
    }

    std::string parse_string() {
        expect('"');
        std::string result;
        while (true) {
            if (pos_ >= text_.size()) throw JsonParseError("unterminated string");
            char c = advance();
            if (c == '"') break;
            if (c == '\\') {
                char esc = advance();
                switch (esc) {
                    case '"': result += '"'; break;
                    case '\\': result += '\\'; break;
                    case '/': result += '/'; break;
                    case 'n': result += '\n'; break;
                    case 't': result += '\t'; break;
                    case 'r': result += '\r'; break;
                    case 'b': result += '\b'; break;
                    case 'f': result += '\f'; break;
                    case 'u': {
                        // Minimal \uXXXX support: emits the raw code point
                        // as a UTF-8-encoded value for the BMP range.
                        if (pos_ + 4 > text_.size()) throw JsonParseError("bad \\u escape");
                        std::string hex = text_.substr(pos_, 4);
                        pos_ += 4;
                        unsigned int code = std::strtoul(hex.c_str(), nullptr, 16);
                        if (code < 0x80) {
                            result += static_cast<char>(code);
                        } else if (code < 0x800) {
                            result += static_cast<char>(0xC0 | (code >> 6));
                            result += static_cast<char>(0x80 | (code & 0x3F));
                        } else {
                            result += static_cast<char>(0xE0 | (code >> 12));
                            result += static_cast<char>(0x80 | ((code >> 6) & 0x3F));
                            result += static_cast<char>(0x80 | (code & 0x3F));
                        }
                        break;
                    }
                    default: throw JsonParseError("invalid escape sequence");
                }
            } else {
                result += c;
            }
        }
        return result;
    }

    JsonValue parse_number() {
        size_t start = pos_;
        if (peek() == '-') advance();
        while (pos_ < text_.size() && std::isdigit(static_cast<unsigned char>(text_[pos_]))) advance();
        if (pos_ < text_.size() && text_[pos_] == '.') {
            advance();
            while (pos_ < text_.size() && std::isdigit(static_cast<unsigned char>(text_[pos_]))) advance();
        }
        if (pos_ < text_.size() && (text_[pos_] == 'e' || text_[pos_] == 'E')) {
            advance();
            if (pos_ < text_.size() && (text_[pos_] == '+' || text_[pos_] == '-')) advance();
            while (pos_ < text_.size() && std::isdigit(static_cast<unsigned char>(text_[pos_]))) advance();
        }
        if (pos_ == start) throw JsonParseError("invalid number at position " + std::to_string(pos_));
        double value = std::strtod(text_.substr(start, pos_ - start).c_str(), nullptr);
        return JsonValue(value);
    }

    JsonValue parse_bool() {
        if (text_.compare(pos_, 4, "true") == 0) {
            pos_ += 4;
            return JsonValue(true);
        }
        if (text_.compare(pos_, 5, "false") == 0) {
            pos_ += 5;
            return JsonValue(false);
        }
        throw JsonParseError("invalid literal at position " + std::to_string(pos_));
    }

    JsonValue parse_null() {
        if (text_.compare(pos_, 4, "null") == 0) {
            pos_ += 4;
            return JsonValue(nullptr);
        }
        throw JsonParseError("invalid literal at position " + std::to_string(pos_));
    }
};

inline JsonValue parse_json(const std::string &text) {
    return JsonParser(text).parse();
}
