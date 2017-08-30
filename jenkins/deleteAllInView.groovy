/**
This script can be copied into the script cinsole in the manage jenkins area of Jenkins

This script does the following:
    get all the jobs in a view
    deletes them

You can change the view to delete from by changing the value of ther variable viewName
**/
def viewName="Test Jobs")
def view = Jenkins.instance.getView(viewName)
def itemsInView = view.getItems()

itemsInView.each{job -> 
    println(job.name)
    job.delete()
}
