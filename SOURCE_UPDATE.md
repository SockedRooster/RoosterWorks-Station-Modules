# Developer source for v0.7.7

The accepted baseline is v0.7.7-test.2. The release changes only the version descriptor inside GameData. StationFlags.cs and StationWiring.cs are in Source. Their development generators in Tools/Development use the original workspace layout and intermediate archives. Run python Tools/package_release.py to verify and package the included release payload.

Historical preview renders are listed in Docs/ARCHIVED_PREVIEWS.txt. To run older visual-review checks, extract those paths from RoosterWorks-Station-Modules-v0.7.6-GitHub-Source.zip into this source folder. They are optional for packaging the current release.
