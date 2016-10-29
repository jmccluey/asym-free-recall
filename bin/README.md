# Experiment executables

These executables provided shortcuts for experiments to run the specific versions of the paradigm, rather than typing a lengthy PyEPL call. For example, to run a session of asymFR3 with participant ASM305, you would type:
```
./asymFR3.sh ASM305
```

As the experiment versions are not backwards-compatible, it is recommended that you download the released version associated with a specific version of the study in order to run it.

_Note:_ These executables assume a standard structure that was present on all lab machines, such that experiments were located in a ~/experiments directory, along with the _expdesign_ and _math_distract_ modules.  You should either follow this assumption, or adjust the experiment dir variables in the shell scripts to point to the appropriate locations.
