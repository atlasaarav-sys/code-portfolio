/*
 * STM32-01 -- Blue Pill Style Dev Board firmware
 *
 * Blinks the user LED (PC13, active-low per ../README.md's schematic:
 * PC13 -> R5 -> D2 -> 3V3) and toggles blink rate when the user button
 * (PA0, active-low, external pull-up) is pressed. This is the reference
 * bring-up firmware for the board every later STM32 project in this repo
 * is physically built on top of.
 *
 * Structured for an STM32CubeIDE/CubeMX-generated project targeting
 * STM32F103C8T6: GPIO init (RCC/GPIO clock enable, pin mode config) is
 * CubeMX boilerplate for this specific board and is left as `MX_GPIO_Init()`
 * (generated, not hand-written here) -- the polling/state logic below is
 * the actual firmware content.
 */

#include "stm32f1xx_hal.h"

#define LED_PIN GPIO_PIN_13
#define LED_PORT GPIOC
#define BUTTON_PIN GPIO_PIN_0
#define BUTTON_PORT GPIOA

static uint32_t blinkPeriodMs = 500;
static uint32_t lastToggleMs = 0;
static GPIO_PinState ledState = GPIO_PIN_SET; // SET = LED off (active-low)

static GPIO_PinState lastButtonReading = GPIO_PIN_SET;
static uint32_t lastDebounceMs = 0;
#define DEBOUNCE_MS 30

/* extern void MX_GPIO_Init(void); // CubeMX-generated, board-specific */

static void handleButton(void) {
    GPIO_PinState reading = HAL_GPIO_ReadPin(BUTTON_PORT, BUTTON_PIN);

    if (reading != lastButtonReading) {
        lastDebounceMs = HAL_GetTick();
    }

    if ((HAL_GetTick() - lastDebounceMs) > DEBOUNCE_MS) {
        static GPIO_PinState debounced = GPIO_PIN_SET;
        if (reading != debounced) {
            debounced = reading;
            if (debounced == GPIO_PIN_RESET) { /* button just pressed (active-low) */
                blinkPeriodMs = (blinkPeriodMs == 500) ? 150 : 500;
            }
        }
    }

    lastButtonReading = reading;
}

int main(void) {
    HAL_Init();
    /* MX_GPIO_Init(); -- configures PC13 as push-pull output, PA0 as input */

    while (1) {
        uint32_t now = HAL_GetTick();

        if (now - lastToggleMs >= blinkPeriodMs) {
            lastToggleMs = now;
            ledState = (ledState == GPIO_PIN_SET) ? GPIO_PIN_RESET : GPIO_PIN_SET;
            HAL_GPIO_WritePin(LED_PORT, LED_PIN, ledState);
        }

        handleButton();
    }
}
