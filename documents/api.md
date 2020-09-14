### Get Light backend version
Get Light backend version information.

```
GET /
```

#### Response
```
Hello! I am the backend of light token, version: 0.01
```

#### Example
```shell
curl https://eid.townway.com.tw:8888/
```

### Generate a new DID account

Generate a new DID account from RSA 1024 key pair. An unused IOTA seed will be create for this account, too.

```
POST /new_did
```


#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key | string | The eID API key (pass with HTTP header) |
| method | string | **Optional.** The DID method, default value is `light`|
| name            | string  | Holder nickname |
| description        | string  | **Optional.** DID meta |
| pub_key  | string | **Optional.** RSA public key or endpoint, service will generate one key-pair if this field is empty. |

#### Response

```json
"LEQNOXPPLCWMORC9VNEA9FMNROECHWVKKVOFLHQUSDXDFYWZBDESS9RWQTYBUJGJQLTWMNJ9DZRP99999"
```

#### Example

```shell
curl https://eid.townway.com.tw:8888/new_did \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 71efe65ae128e4562fdba2292b2b3f190845c7h3' \
    -d '{"method": "light", "name": "tim", "description": "Zhushan light eID", "pub_key":""}'
```

### Get DID
Get a DID description from Tangle.

```
GET /did
```

#### Response
```json
{"method": "light", "name": "tim", "description": "Zhushan light eID", "pub_key": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCTuqLOt4jpVFdxh6Lynb45dmll\ngcUBk70WzKlUPzXqIacwQJsGvYJ+Ks20slB62hCxP0Ynk/MBru+3cnLNxCtfcbBY\nN/F3bVaL0LNi2m6P40tOjSOXhO+DTpci6i1wxaFflHwq9GekMAp0MDZY9Jje9xSS\nlgjFwnHcomeh6ksANwIDAQAB\n-----END PUBLIC KEY-----"}
```

#### Example
```shell
curl https://eid.townway.com.tw:8888/did?hash=LEQNOXPPLCWMORC9VNEA9FMNROECHWVKKVOFLHQUSDXDFYWZBDESS9RWQTYBUJGJQLTWMNJ9DZRP99999\
```

### Set layer-1
Set a username to layer-1.

```
GET /set_layer1
```

#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key | string | The CB eID API key (pass with HTTP header) |

#### Response
"OK"

#### Example
```shell
curl https://eid.townway.com.tw:8888/set_layer1?username=john \
        -H 'X-API-key: 95efe65ae128e4562fdba2292b2b3f190845c503' 
```

### Remove layer-1
Remove a username from layer-1
```
DELETE /remove_layer1
```

#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key | string | The CB eID API key (pass with HTTP header) |

#### Response
"Remove + username"

#### Example
```shell
curl -X DELETE http://localhost:8888/remove_layer1?username=zoo -H 'X-API-key: 95efe65ae128e4562fdba2292b2b3f190845c503'
```

### Send token
Send token.

```
POST /send_token
```

#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key   | string | The sender or CB eID API key (pass with HTTP header) |
| sen         | string | The sender CB ID |
| rev         | string | Receiver ID |
| method      | string | Transaction method, should be 1 |
| description | string | Transaction comment |
| txn         | string | **Should be null on layer-1.** Token txn hash |

#### Response
Token transaction hash

#### Example (layer-1)
```shell
curl https://eid.townway.com.tw:8888/send_token \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 95efe65ae128e4562fdba2292b2b3f190845c503' \
    -d '{"sen": "cb", "rev": "john", "method": "1", "description": "Light token", "txn":""}'
```

#### Example (layer-2)
```shell
curl https://eid.townway.com.tw:8888/send_token \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 95efe65ae128e4562fdba2292b2b3f190845c503' \
    -d '{"sen": "john", "rev": "mary", "method": "2", "description": "Light token" , "txn":"X99KHARMXNVFRDSKBIBFVBYSXRDMZRLYUHWNET9PJHXPIJUWEKWVQWGPHABKYRTKYVJXJWULDEKE99999"}'
```
### Send multiple tokens.
Send tokens.
```
POST /send_tokens
```
#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key   | string | The sender or CB eID API key (pass with HTTP header) |
| sen         | string | The sender CB ID |
| rev         | string | Receiver ID |
| method      | string | Transaction method, **only support 2** |
| description | string | Transaction comment |
| txn         | string[] | Array of Token txn hash |
#### Response
Token transactions hash

#### Example
```shell
curl https://eid.townway.com.tw:8888/send_tokens \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 95efe65ae128e4562fdba2292b2b3f190845c503' \
    -d '{"sen": "bchen", "rev": "john", "method": "2", "description": "Light token", "txn":["VQDMVAOUMFPMADDJHGMVKGQZWDDBPLJXMKPMGOHQDBMQFYTVNMKZGSZITNFBRIH9WFOBT9XBTEEXA9999","DW9OVOH9FZSOKY9TPWAWYSCVOUZQLYHYTQZIZSMFFXSTXJAQCMBWTSJLDXRUBDDGZLOYAWRZXRFMA9999"]}'
```
### Get balance
Get account token balance.

```
GET /get_balance
```

#### Response
```
ACYAMYALANWRZVOPRDWALLVJKXJGZDVGDSDAYGROETUHTULVWIO9MOWOXVHFBSTCXEFGDVDOURWU99999
VIYDURPULV9OWBBKF9BQKPQHARUNLXNOCXBYZRTTBQGFSNPNZTZKFKILWRHVDIFOLAUYHUAWNGZL99999

```

#### Example
```shell
curl https://eid.townway.com.tw:8888/get_balance?user=mary
```

### Verify token
Verify self-token.

```
POST /verify_token
```

#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key   | string | The token owner eID API key (pass with HTTP header) |
| user        | string | Username |
| token       | TRYTES | The token IOTA transaction hash |

#### Response
``` json
{"status": "valid"}
```

#### Example
```shell
curl https://eid.townway.com.tw:8888/verify_token \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 88efe65ae128e4562fdba2292b2b3f190845c7h3' \
    -d '{"user": "mary", "token": "UXKZCZHQJCPAFPNWTSLXRVSBMNOFZUFAIRBYIUEFATDMKKKYELYP9ADTNXRIHUZFIRNWMDCDTUISZ9999"}'                                                                                                                            
```

### Snapshot
Token snapshot.

```
POST /snapshot
```

#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key   | string | The token owner eID API key (pass with HTTP header) |
| user        | string | Username |
| token       | TRYTES | The token IOTA transaction hash |

#### Response
```
XNI9GDT9CRNOYBNFHLKXWRFPNACBZUFSXXOBRVDBJIIRGZZNNYIYZELWYVMPDTOIZGNQYEI9GQKIA9999
```

#### Example
```shell
curl https://eid.townway.com.tw:8888/snapshot \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 88efe65ae128e4562fdba2292b2b3f190845c7h3' \
    -d '{"user": "mary", "token": "AMXFRD9URKGRGMEUGESBMOQKCEWKJMRKQDSXKTJKCBAZIAQPZRA9TR9TGXGKOXENPAPFIXFQAQMW99999"}'                                                                                                               
```

### Get all cluster
Get all economic cluster.

```
GET /get_all_cluster
```

#### Response
``` json
{
  "cb": "EWKGAQUPUPED9TSKKOPQVTPUKDHJOPJJVDKXMWOBOFWLYRRFZKBIBYGVODTQPGCIDRQZEQSWGWBVZ9999", 
  "layer-1": [
    "ZHUNCIRFBUHWWCPRKRSUQBPSKORPEOZJJSMSOGZDSUQGKDVRKGOHIEMUW9DDQULABAXWZRLGRBXJZ9999"
  ]
}
```

#### Example
```shell
curl https://eid.townway.com.tw:8888/get_all_cluster
```

### Bridge
Bridge token.

```
POST /bridge
```

#### Parameters
| Name           | Type    | Description                                                                                                                                                                                                 |
| -------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-API-key   | string | The token owner eID API key (pass with HTTP header) |
| name        | string | sender |
| rev         | string | receiver |

#### Response
New token hash.
```
99RQSRXZLTKAYDXWHCECIZNRFCVEXIYGAFRQVETLIWMAPIYIXTPAGGEIHUHWTMBCBRZDESVCHGZWA9999
```

#### Example
```shell
curl https://eid.townway.com.tw:8888/bridge \
    -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 95efe65ae128e4562fdba2292b2b3f190845c503' \
    -d '{"name":"john", "rev":"mary"}'
```
