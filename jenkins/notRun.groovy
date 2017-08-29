/** 
This script can be copied into the script console in the manage Jenkins area of Jenkins

This script does the following:
    clears the view "old_Jobs"
    searches through all the jobs and adds any jos which haven't been executed in the last 90 days to a new view

You can change the number of days by change the value of ther day variable
*/
day=90
hour=24;
minute=60;
second=60;
daysInSecond=day*hour*minute*second;
now=Calendar.instance;

def view = Jenkins.instance.getView("Old_Jobs")
def itemsInView = view.getItems()

itemsInView.each{job ->
    view.remove(job)
}

allJobs = jenkins.model.Jenkins.instance.items
def count = 0
allJobs.each{run -> 
    def lastBuild = run.getLastBuild()
    if(lastBuild != null){  
        def lastBuildTime = lastBuild.getTimestamp().time.time
        if(now.time.time/1000-lastBuildTime/1000>daysInSecond){
            println("https://fem119-eiffel004.lmera.ericsson.se:8443/jenkins/view/All/job/$run.name"); 
            println("\tLast run: $lastBuild.time");
            count++;
            view.add(run)
        }
    } else {
        println("https://fem119-eiffel004.lmera.ericsson.se:8443/jenkins/view/All/job/$run.name") 
        println("\tLast run: never!");
        count++
        view.add(run)
    }
}
println("Total # of jobs not run in 90 days is: $count")
