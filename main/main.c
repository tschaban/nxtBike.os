#include <inttypes.h>

#include "esp_chip_info.h"
#include "esp_app_desc.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "esp_psram.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "nxtbike";

void app_main(void)
{
    esp_chip_info_t chip;
    esp_chip_info(&chip);

    ESP_LOGI(TAG, "nxtBike.os %s starting", esp_app_get_description()->version);
    ESP_LOGI(TAG, "CPU cores: %d, silicon revision: %d", chip.cores,
             chip.revision);
    ESP_LOGI(TAG, "PSRAM: %u bytes", (unsigned)esp_psram_get_size());

    // Hardware drivers and application services will be added incrementally.
    for (;;) {
        ESP_LOGI(TAG, "Heartbeat; free internal heap: %" PRIu32 " bytes",
                 (uint32_t)heap_caps_get_free_size(MALLOC_CAP_INTERNAL |
                                                 MALLOC_CAP_8BIT));
        vTaskDelay(pdMS_TO_TICKS(10000));
    }
}
