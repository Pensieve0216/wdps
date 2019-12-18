
ES_PORT=9200
ES_BIN=/home/jurbani/wdps/elasticsearch-2.4.1/bin/elasticsearch

prun -o .es_log -v -np 1 ESPORT=$ES_PORT $ES_BIN </dev/null 2> .es_node &
echo "Waiting for 15 seconds elasticsearch to set up..."
sleep 15
ES_NODE=$(cat .es_node | grep '^:' | grep -oP '(node...)')
ES_PID=$!
echo "Elasticsearch should be running now on node $ES_NODE:$ES_PORT (connected to process $ES_PID)"

python3 elasticsearch.py node001:$ES_PORT "Vrije Universiteit Amsterdam"

kill $ES_PID