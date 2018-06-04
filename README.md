# crackMd5
Pyopencl brute-forcer for md5 hashes

To show available opencl devices:

```python crack.py --showdevices```

To launch brute-force:

```python crack.py --hash=%hash_value_in_hex% --dict=%path_to_dictionary% --devices=%comma_separated_list_of_device_numbers%```

e.g.:

```python crack.py --hash=6ee6a213cb02554a63b1867143572e70 --dict=dict.txt --devices=0,1```

If launched without `--dict` argument, checks random passwords. Could be used for measuring speeds on different devices.
