.DEFAULT_GOAL := copy

.user    := pi
.machine := pi3.local
.env     := /home/pi/.virtualenvs/cv/bin/activate
.dir     := scripts

help:
	@echo ""
	@echo "Available commands :"
	@echo ""
	@echo "  make \t\t\t\tcopies current directory"
	@echo "  make copy\t\t\tcopies current directory"
	@echo "  make install\t\t\tinstalls Python dependencies"
	@echo "  make exec PROGRAM=<program>\texecutes the program"
	@echo ""

copy:
	rsync -r ./* $(.user)@$(.machine):~/scripts

install: copy
	ssh $(.user)@$(.machine) " \
	source $(.env); \
	pip install -r $(.dir)/requirements.txt"

exec:
	ssh $(.user)@$(.machine) " \
	source $(.env); \
	if pgrep -u $(.user) python; then pkill -u $(.user) python; fi; \
	python $(.dir)/programs/$(PROGRAM).py &"

stop:
	ssh $(.user)@$(.machine) "pkill -u $(.user) python"

.PHONY: copy install exec stop
