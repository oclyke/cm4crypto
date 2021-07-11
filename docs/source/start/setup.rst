Setup of the cm4crypto is very similar to setup of a typical raspberry pi computer. 

flashing an operating system
----------------------------

Most of the time standard Raspberry Pi boards use the SD card to store the operating system (OS). 
When using the Compute Module 4 (cm4) you will either store the OS on an SD card or on internal eMMC
memory, depending on the options you've selected when you purchased the module.

.. note::
   Compute modules with eMMC storage **cannot** boot from the SD card. 
   Check this Raspberry Pi forum post for more detail: 
   `Can CM4 with eMMC boot from SD card <https://www.raspberrypi.org/forums/viewtopic.php?t=305506>`_

eMMC
^^^^

The eMMC memory module will act a lot like an SD card would when setting up a normal Raspberry Pi except
you can't simply take it out and put it in your computer. Instead the Compute Module needs to be put
into *bootloader* mode which will mount the eMMC on your computer as a USB mass storage device. Then it
can be used just like a normal RPi SD card.

To mount the eMMC as USB mass storage device:

* download `raspberrypi/usbboot <https://github.com/raspberrypi/usbboot>`_

* turn the **BOOT** switch on cm4crypto to ``MSD``
* turn the **USB** switch on cm4crypto ``C``
* plug in cm4crypto to your computer via the USB-C port
   * the Compute Module should turn on in boot mode awaiting the next steps

The next step depends on your computer's operating system

.. note:: *Windows*

   * use **rpiboot_setup.exe** to install required drivers and boot tool
   * start **rpiboot.exe**

.. note:: *Linux / OSX*

   * install libusb

      * Linux: ``apt install -y libusb-1.0.0-dev``
      * OSX: ``brew install libusb``
      
   * build the executable in the ``raspberrypi/usbboot`` root directory ``make``
   * run the rpiboot executable ``./rpiboot``

* now the Compute Module should appear on your computer as a removable drive called ``boot``
* proceed to flash your desired operating system on this drive using your preferred tool

   * `Raspberry Pi Imager <https://www.raspberrypi.org/software/>`_
   * `Balena Etcher <https://www.balena.io/etcher/>`_

.. note:: Initially your computer may give you an error like 

   ``the disk you inserted was not able to be read by the system``

   this is because the disk is not formatted and will not affect the image writing tool's 
   ability to flash the OS

* once the image is flashed you may choose to do optional configuration or skip straight to the first boot.

Jeff Geerling made an excellent video about the process which you can see here:

.. raw:: html
   
   <iframe
      width="100%"
      height="475"
      src="https://www.youtube.com/embed/jp_mF1RknU4"
      title="YouTube video player"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen>
   </iframe>

SD
^^

* insert an SD card in your computer

   * it should appear as a removable storage device

* flash your desired operating system on this drive using your preferred tool

   * `Raspberry Pi Imager <https://www.raspberrypi.org/software/>`_
   * `Balena Etcher <https://www.balena.io/etcher/>`_

* once the image is flashed you may choose to do optional configuration or skip straight to the first boot



optional configuration
----------------------

Once you have flashed the OS to your Compute Module you may perform some initial configuration by modifying 
files on the eMMC boot drive / SD card. This is especially useful for configuring a headless machine.

enable USB2.0 host controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unlike the Raspberry Pi the Compute Module 4 leaves its USB2.0 host controller disabled by default to save power. 
In order to use the USB-A port on the cm4crypto you must add the following line to the **boot/config.txt** file. 
If you choose not to do this now it will still be possible by editing **/boot/config.txt** while the Pi is running. 
Changes will take effect on the next boot up.

``dtoverlay=dwc2,dr_mode=host``

enabling ssh
^^^^^^^^^^^^

SSH can be used control the Pi remotely, relying on the display and keyboard of another computer, but it is
disabled by default. To enable it you must simply add a file called **ssh** in the boot directory. (The root of the removable storage device)

enable wifi
^^^^^^^^^^^

* add **wpa_supplicant.conf** in the boot partition (**/boot**)

   * [raspberry pi foundation documentation](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
   * [stack overflow multiple network config](https://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks)

**example**
::

   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   country=<Insert 2 letter ISO 3166-1 country code here>
   update_config=1

   network={
      ssid="<name of your wireless LAN>"
      psk="<password for your wireless LAN>"
      id_str="<identifier for your wireless LAN>"
   }

   network={
      ssid="<name of another wireless LAN>"
      psk="<password for the other wireless LAN>"
      id_str="<identifier for the other wireless LAN>"
   }


enable camera interface
^^^^^^^^^^^^^^^^^^^^^^^

The Compute Module also ships without support for the camera interface enabled. To get the camera working
you need to add a device tree configuration blob to the root file system.

To generate the file yourself follow the `documentation <https://www.raspberrypi.org/documentation/hardware/computemodule/cmio-camera.md>`_

To get started faster you can use the generic file ``dt-blob.bin`` in the ``device-tree`` directory of the `cm4crypto repository <https://github.com/subluminal-li/cm4crypto>`_


change the pi user's password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default password for the ``pi`` user is insecure (it is all over the internet!). There are several 
strategies for mending this security concern without exposing your computer to the public internet for
any duration unprotected.

Get started with `this thread <https://www.raspberrypi.org/forums/viewtopic.php?t=289155>`_


first boot
----------

* remove power from the board
* ensure that the **BOOT** switch is in the ``NOM`` position

   * remember - if you want to use the USB-A host port ensure the **USB** switch is in the ``A`` position

* plug in any peripherals you want to use (HDMI, USB, etc)
* apply power
