#include <cassert>
#include <cstdio>

#include "json_parser.hpp"

int main() {
    std::string text = R"({
        "name": "telemetry-session-42",
        "duration_s": 180.5,
        "passed": true,
        "notes": null,
        "signals": ["speed_mph", "battery_voltage", "motor_temp_c"],
        "thresholds": {"motor_temp_c": 80, "battery_voltage": 40}
    })";

    JsonValue root = parse_json(text);

    assert(root.is_object());
    assert(root.find("name")->as_string() == "telemetry-session-42");
    assert(root.find("duration_s")->as_number() == 180.5);
    assert(root.find("passed")->as_bool() == true);
    assert(root.find("notes")->is_null());
    assert(root.find("signals")->as_array().size() == 3);
    assert(root.find("thresholds")->find("motor_temp_c")->as_number() == 80);

    std::printf("Parsed fields:\n");
    std::printf("  name: %s\n", root.find("name")->as_string().c_str());
    std::printf("  duration_s: %.1f\n", root.find("duration_s")->as_number());
    std::printf("  passed: %s\n", root.find("passed")->as_bool() ? "true" : "false");
    std::printf("  signals[0]: %s\n", root.find("signals")->as_array()[0].as_string().c_str());

    std::printf("\nRound-tripped JSON:\n%s\n", root.dump().c_str());

    // Round-trip: re-parse the dumped output and check it still matches.
    JsonValue reparsed = parse_json(root.dump());
    assert(reparsed.find("name")->as_string() == "telemetry-session-42");

    std::printf("\nAll assertions passed.\n");
    return 0;
}
