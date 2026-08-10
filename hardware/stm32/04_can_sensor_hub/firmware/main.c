/*
 * STM32-04 -- CAN + USB-C Sensor Hub firmware
 *
 * Reads an IMU over I2C and broadcasts it on the CAN bus as a standard
 * CAN frame every 20ms, with a USB-CDC debug console mirroring the same
 * data -- this is the "sensor node on a CAN network" firmware the board
 * is designed for (see ../README.md for the network/power architecture).
 *
 * Structured for an STM32CubeIDE/CubeMX-generated STM32F405 project with
 * bxCAN + USB_DEVICE (CDC) enabled. Peripheral/middleware init
 * (`MX_CAN1_Init`, `MX_I2C1_Init`, `MX_USB_DEVICE_Init`) is CubeMX
 * boilerplate, left as comments -- the CAN framing and I2C read logic
 * below is the real content.
 *
 * Pin mapping (see ../README.md section 1):
 *   CAN1: TXD=PB9, RXD=PB8 -> TJA1051T/3 transceiver -> CANH/CANL
 *   I2C1: SCL=PB6, SDA=PB7 -> ICM-42688-P IMU (addr 0x68)
 *   USB FS (PA11/PA12) -> USB-CDC debug console
 */

#include <stdio.h>

#include "stm32f4xx_hal.h"
#include "usbd_cdc_if.h"

extern CAN_HandleTypeDef hcan1;
extern I2C_HandleTypeDef hi2c1;

#define IMU_I2C_ADDR (0x68 << 1) /* HAL I2C addresses are left-shifted by 1 */
#define IMU_REG_ACCEL_XOUT_H 0x1F /* ICM-42688-P accel data start register */
#define CAN_TX_ID 0x100           /* arbitrary node ID on the bus; assign per-node in a real network */

typedef struct {
    int16_t accelX, accelY, accelZ;
} ImuReading;

static HAL_StatusTypeDef readImu(ImuReading *out) {
    uint8_t raw[6];
    HAL_StatusTypeDef status = HAL_I2C_Mem_Read(&hi2c1, IMU_I2C_ADDR, IMU_REG_ACCEL_XOUT_H,
                                                 I2C_MEMADD_SIZE_8BIT, raw, sizeof(raw), 50);
    if (status != HAL_OK) return status;

    out->accelX = (int16_t)((raw[0] << 8) | raw[1]);
    out->accelY = (int16_t)((raw[2] << 8) | raw[3]);
    out->accelZ = (int16_t)((raw[4] << 8) | raw[5]);
    return HAL_OK;
}

static void sendImuOverCan(const ImuReading *reading) {
    CAN_TxHeaderTypeDef header = {
        .StdId = CAN_TX_ID,
        .IDE = CAN_ID_STD,
        .RTR = CAN_RTR_DATA,
        .DLC = 6,
    };
    uint8_t payload[6] = {
        (uint8_t)(reading->accelX >> 8), (uint8_t)reading->accelX,
        (uint8_t)(reading->accelY >> 8), (uint8_t)reading->accelY,
        (uint8_t)(reading->accelZ >> 8), (uint8_t)reading->accelZ,
    };

    uint32_t mailbox;
    HAL_CAN_AddTxMessage(&hcan1, &header, payload, &mailbox);
}

static void logOverUsb(const ImuReading *reading) {
    char line[64];
    int len = snprintf(line, sizeof(line), "accel: x=%d y=%d z=%d\r\n",
                        reading->accelX, reading->accelY, reading->accelZ);
    CDC_Transmit_FS((uint8_t *)line, len);
}

int main(void) {
    HAL_Init();
    /* MX_GPIO_Init(); MX_I2C1_Init(); MX_CAN1_Init(); MX_USB_DEVICE_Init(); */

    HAL_CAN_Start(&hcan1);

    while (1) {
        ImuReading reading;
        if (readImu(&reading) == HAL_OK) {
            sendImuOverCan(&reading);
            logOverUsb(&reading);
        }
        HAL_Delay(20); /* 50 Hz update rate */
    }
}
