for RACK in 105 108 136; do
	for UNIT in $(seq 1 19); do
		for BLADE in 1 2 3 4; do
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_general24"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_general72"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_interactive"
		done
	done
done

for RACK in 106; do
	for UNIT in $(seq 1 19); do
		for BLADE in 1 2 3 4; do
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_throughput24"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_throughput72"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_interactive"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_debug"
		done
	done
done

for RACK in 101; do
	for UNIT in $(seq 1 19); do
		for BLADE in 1 2 3 4; do
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_singlenode24"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_interactive"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_debug"
		done
	done
done


for RACK in 130; do
	for UNIT in $(seq 1 5); do
		for BLADE in $(seq 1 20); do
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_multinode24"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_multinode48"
		done
	done
done

for RACK in 50; do
	for UNIT in 3; do
		for BLADE in $(seq 1 15) $(seq 19 29); do
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_largemem24"
			qmgr -c "set node cx1-${RACK}-${UNIT}-${BLADE} resources_available.Qlist += v1_largemem48"
		done
	done
done

for NODE in 15-4-1 15-4-5 15-4-6 51-5-1; do
			qmgr -c "set node cx1-${NODE} resources_available.Qlist += v1_gpu24"
			qmgr -c "set node cx1-${NODE} resources_available.Qlist += v1_gpu48"
done

