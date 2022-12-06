# MoeGoe Simple API Server

See [MoeGoe](https://github.com/CjangCjengh/MoeGoe)

## API Reference

-----------

GET `/tts`

| parameter   | default     |
| ----------- | ----------- |
| text | `None` |
| speaker | 0 |
|length_scale|1.1|
|noise_scale| 0.667|
|noise_scale_w|0.8|

* returns wav file

-----------
 
GET `/list`
* returns list of speakers