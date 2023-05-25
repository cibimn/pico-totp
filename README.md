# Raspberry Pi Pico/MicroPython 2FA TOTP Generator with RTC

Generates Time-based One-Time Password's (TOTP) using MicroPython, Raspberry Pi Pico and the [Pico Display Pack](https://shop.pimoroni.com/products/pico-display-pack).

## Features

- Complete [MicroPython implementation](totp) of the TOTP specification (and underlying HMAC-SHA1, Base32 dependencies).
- Customisable background colours per TOTP.
- Progress bar to present how long till the TOTP is about to expire.
- Flashing alert LED when the TOTP is about to expire.
- Added Waveshare Precision RTC Module DS3231 Chip to maintain clock

## Usage

- Connect the [Pico Display Pack](https://shop.pimoroni.com/products/pico-display-pack) to the Raspberry Pi Pico.
- Create a `codes.json` file (based on `codes.json`) which includes the desired TOTP keys.
- Flash the Raspberry Pi Pico with the 0.3.2 version as the code is not updated to the latest version.
- Copy the codebase to the Raspberry Pi Pico.
- Now you can cycle through your TOTP's using the `X` and `Y` button.

Thanks to [Eddmann](https://github.com/eddmann) built this on top of [pico-2fa-totp](https://github.com/eddmann/pico-2fa-totp)