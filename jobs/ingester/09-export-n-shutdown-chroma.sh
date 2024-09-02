#!/bin/sh
### EXAMPLE
## 이 친구는, Chroma가 network layer로 넘어가면 

## Shutdown chroma
chroma shutdown


## Export data to vessl artifact and link it to the knowledge
DB_SOURCE_PATH="$(pwd)/chroma-data"
python script/export_chroma_data.py --db-source-path $DB_SOURCE_PATH