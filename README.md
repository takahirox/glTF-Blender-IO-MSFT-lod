# glTF-Blender-IO-MSFT-lod

**glTF-Blender-IO-MSFT-lod** is a [Blender](https://www.blender.org/) addon for [glTF `MSFT_lod` extension](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Vendor/MSFT_lod/README.md) on top of [`glTF-Blender-IO`](https://github.com/KhronosGroup/glTF-Blender-IO) addon.

## Compatible Blender version

&gt;= 3.3

## Features

The addon enables to import and export glTF assets with the [glTF `MSFT_lod` extension](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Vendor/MSFT_lod/README.md) in Blender.

## How to install

### Ensure the `glTF-Blender-IO` addon is installed and enabled

Ensure the `glTF-Blender-IO` addon is installed and enabled in your Blender because the `glTF-Blender-IO-MSFT-lod` addon works on top of it.  You can check it by Edit -> Preferences -> Add-ons -> "glTF 2.0" in the search bar. The `glTF-Blender-IO` addon should be listed as `Import-Export: glTF 2.0 format`. It should be installed and enabled by default.

![Ensure glTF-Blender-IO is installed and enabled](https://user-images.githubusercontent.com/7637832/110406787-a41f3f80-8037-11eb-9e12-163aafd5f08e.png)

### Download the zip archived source code

Download the zip archived source code from the [Releases](https://github.com/takahirox/glTF-Blender-IO-MSFT-lod/releases).

### Install `glTF-Blender-IO-MSFT-lod` addon

Install the `glTF-Blender-IO-MSFT-lod` addon to your Blender via Edit -> Preferences -> Add-ons -> Install -> Select the downloaded file

![Edit -> Preferences](https://user-images.githubusercontent.com/7637832/110405180-062a7580-8035-11eb-839a-f5008a992f92.png)

![Add-ons -> Install](https://user-images.githubusercontent.com/7637832/110405413-70dbb100-8035-11eb-9860-3f4867427246.png)

![Select the downloaded file](https://user-images.githubusercontent.com/7637832/193182063-6f7476f8-a8ae-4bb9-ab5f-7e3ba0cb020c.png)

### Enable the addon

Ensure the addon is installed and enabled. You can easily find the addon by inputting "MSFT_lod" in the search bar. Check the checkbox to enable the addon.

![Ensure the addon is enabled](https://user-images.githubusercontent.com/7637832/193182303-27e29b32-1e36-49c6-9a9a-7585113159b9.png)

## How to use

The addon adds the "Level Of Details" panel to the Object property. You can add, remove, and edit the LODs for an object in the panel. And the addon imports the LODs defined with the `MSFT_lod` extension to the panel. And the LODs configuration in the panel is exported as `MSFT_lod` extension when you export assets as glTF/glb.

![Level of Details panel](https://user-images.githubusercontent.com/7637832/193184055-2ce6499a-0a95-47f6-bd52-5d687117f0fc.png)

## Limitations

* Currently the addon supports LOD only under node, doesn't support it under material. [#1](https://github.com/takahirox/glTF-Blender-IO-MSFT-lod/issues/1)
