#include <Arduino.h>

// Retain application identity in both profiles, including builds without logs.
extern "C" const char nxtbike_firmware_version[] = NXTB_FIRMWARE_VERSION;

void setup()
{
#if NXTB_DIAGNOSTICS
    Serial.begin(115200);
    Serial.printf("nxtBike.os %s starting\n", nxtbike_firmware_version);
    Serial.printf("CPU cores: %u, silicon revision: %u\n",
                  ESP.getChipCores(), ESP.getChipRevision());
    Serial.printf("PSRAM: %u bytes\n", ESP.getPsramSize());
#endif
}

void loop()
{
#if NXTB_DIAGNOSTICS
    Serial.printf("Heartbeat; free internal heap: %u bytes\n", ESP.getFreeHeap());
#endif
    delay(10000);
}
