/*
 * STM32-02 -- Dual Motor Driver Board firmware
 *
 * Open-loop PWM speed/direction control for two DC motors via a DRV8833
 * dual H-bridge (TIM1 PWM outputs), with quadrature encoder feedback read
 * in hardware timer encoder mode (TIM2/TIM4) -- this file wires up the
 * open-loop drive + encoder readback; closing the loop (PID on encoder
 * counts -> PWM duty) is the natural next step once this bring-up works.
 *
 * Structured for an STM32CubeIDE/CubeMX-generated STM32F401 project.
 * Peripheral init (RCC/GPIO/TIM handle setup, encoder mode config) is
 * left as CubeMX boilerplate (`MX_TIM1_Init`, `MX_TIM2_Init`,
 * `MX_TIM4_Init`, `MX_GPIO_Init`) since it's project-config-specific --
 * the motor control math and encoder readback below are the real content.
 *
 * Pin mapping (see ../README.md section 1):
 *   TIM1_CH1-4 (PA8-PA11) -> DRV8833 AIN1/AIN2/BIN1/BIN2
 *   TIM2_CH1/CH2 (PA0/PA1) -> Encoder A quadrature
 *   TIM4_CH1/CH2 (PB6/PB7) -> Encoder B quadrature
 *   PB0 -> DRV8833 nSLEEP, PB1 -> DRV8833 nFAULT (input)
 *   PA15 -> E-stop / mode button
 */

#include "stm32f4xx_hal.h"

extern TIM_HandleTypeDef htim1; /* PWM: 4 channels driving the H-bridge */
extern TIM_HandleTypeDef htim2; /* Encoder A, hardware encoder mode */
extern TIM_HandleTypeDef htim4; /* Encoder B, hardware encoder mode */

#define PWM_MAX_DUTY 999 /* TIM1 ARR, set in CubeMX for the desired PWM frequency */

typedef struct {
    uint32_t channelForward;
    uint32_t channelReverse;
} MotorChannels;

static const MotorChannels MOTOR_A = {TIM_CHANNEL_1, TIM_CHANNEL_2}; /* AIN1, AIN2 */
static const MotorChannels MOTOR_B = {TIM_CHANNEL_3, TIM_CHANNEL_4}; /* BIN1, BIN2 */

/* speedPercent in [-100, 100]: sign = direction, magnitude = duty cycle. */
static void setMotorSpeed(const MotorChannels *motor, int8_t speedPercent) {
    if (speedPercent > 100) speedPercent = 100;
    if (speedPercent < -100) speedPercent = -100;

    uint32_t duty = (uint32_t)((speedPercent < 0 ? -speedPercent : speedPercent) * PWM_MAX_DUTY / 100);

    if (speedPercent >= 0) {
        __HAL_TIM_SET_COMPARE(&htim1, motor->channelForward, duty);
        __HAL_TIM_SET_COMPARE(&htim1, motor->channelReverse, 0);
    } else {
        __HAL_TIM_SET_COMPARE(&htim1, motor->channelForward, 0);
        __HAL_TIM_SET_COMPARE(&htim1, motor->channelReverse, duty);
    }
}

static int32_t readEncoderCount(TIM_HandleTypeDef *encoderTimer) {
    /* TIM_CNT is a free-running 16-bit counter in encoder mode; cast to
       int16_t so it wraps/reads as a signed relative position delta. */
    return (int16_t)__HAL_TIM_GET_COUNTER(encoderTimer);
}

int main(void) {
    HAL_Init();
    /* MX_GPIO_Init(); MX_TIM1_Init(); MX_TIM2_Init(); MX_TIM4_Init(); */

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET); /* nSLEEP high = driver active */

    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_4);
    HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL);
    HAL_TIM_Encoder_Start(&htim4, TIM_CHANNEL_ALL);

    while (1) {
        if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_15) == GPIO_PIN_RESET) { /* E-stop pressed */
            setMotorSpeed(&MOTOR_A, 0);
            setMotorSpeed(&MOTOR_B, 0);
            HAL_Delay(50);
            continue;
        }

        if (HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_1) == GPIO_PIN_RESET) { /* nFAULT active-low */
            setMotorSpeed(&MOTOR_A, 0);
            setMotorSpeed(&MOTOR_B, 0);
            continue; /* driver reports a fault -- stay stopped until it clears */
        }

        /* Demo open-loop pattern: ramp motor A forward, hold motor B still.
           Replace with real control input (serial command, PID setpoint, etc). */
        setMotorSpeed(&MOTOR_A, 40);
        setMotorSpeed(&MOTOR_B, 0);

        int32_t encoderACount = readEncoderCount(&htim2);
        int32_t encoderBCount = readEncoderCount(&htim4);
        (void)encoderACount;
        (void)encoderBCount; /* feed these into a PID loop for closed-loop control */

        HAL_Delay(10);
    }
}
