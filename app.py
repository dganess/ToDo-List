
import sqlite3
from bottle import run, route, template, request, view, debug, redirect, error
#test commit
@route('/')
@view('index')
def index():
    pass
# heloo world
#------------------------------------------------------------------------------------------------------------
# Find Item to Edit Block
#------------------------------------------------------------------------------------------------------------
@route('/find_item', method = 'GET')   # executed from index.html and button 'edit item in Todo list' pressed
def show_all_items():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo")
    result = c.fetchall()             # fetches all items in Todo database and stores data in variable 'result'
    c.close()
    
    return template('find_edit_item.tpl',rows=result) # sends result data to template to display all items in todo list and choose item to edit


@route('/find_item', method = 'POST')   # returns edit item ID and stores in variable edit_id
def edit_item_found():
    edit_id = request.POST.get('todoID','').strip()
    redirect('/edit/{}'.format(edit_id))

@route('/edit/<no:int>')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()              #returns task from edit template and stores in variable 'edit' to update Database#
        status = request.GET.status.strip()         # returns status from edit template and stores in variable 'status' to update Database

        if status == 'open':                    
            status = 1                              # stores appropriate value to update status value in Database
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))   # queries Database and updates entry
        conn.commit()                           # writes data to file

        return template('edit_exit.tpl',no=no)  # after editing, displays template for confirmation message and button to return to index page
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchone()

        if not cur_data:
            redirect('/invalid_item')

        return template('edit_task.tpl', old=cur_data, no=no)    # template to display item for editing


#------------------------------------------------------------------------------------------------------------
# Find Item to Delete Block
#------------------------------------------------------------------------------------------------------------

@route('/delete_item', method = 'GET')   # executed from index.html and button 'edit item in Todo list' pressed
def show_all_items():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo")
    result = c.fetchall()             # fetches all items in Todo database and stores data in variable 'result'
    c.close()
    
    return template('find_delete_item.tpl',rows=result) # sends result data to template to display all items in todo list and choose item to edit

@route('/delete_item', method = 'POST')   # returns delete item ID and stores in variable delete_id
def delete_item_found():
    delete_id = request.POST.get('todoID','').strip()
    redirect('/delete/{}'.format(delete_id))   # redirects to delete function passing delelte_id

@route('/delete/<no:int>')
def delete_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'Yes':
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute("Delete FROM todo where id = ?", (str(no),))
            conn.commit()
            c.close()
        else:
            return str('not deleted')
        return template('delete_exit.tpl',no=no)
    

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchone()
        if not cur_data:
            redirect('/invalid_item')


        return template('delete_task.tpl', old=cur_data, no=no)    


#------------------------------------------------------------------------------------------------------------
# Displays all Outstanding items from Database ie where status is 1 or open
#------------------------------------------------------------------------------------------------------------

@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    #return str(result)
    output = template('make_table.tpl', rows=result)
    return output
#------------------------------------------------------------------------------------------------------------
# Displays all items from Database
#------------------------------------------------------------------------------------------------------------
@route('/todo_all')
def todo_list_all():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task, status FROM todo") # queries all fields from database and stores as LIST of tuples in variable result
    result = c.fetchall()
    c.close()
    print(result)
    output = template('make_table.tpl', rows=result)
    return output

#------------------------------------------------------------------------------------------------------------
# Add new item Block
#------------------------------------------------------------------------------------------------------------
@route('/new', method='GET')
@view('new_task')
def new_item():
    if request.GET.save:

        new = request.GET.task.strip()

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
        new_id = c.lastrowid

        conn.commit()
        c.close()
        
        return template('new_exit.tpl',new_id=new_id)
    else:
        return template('new_task.tpl')

#------------------------------------------------------------------------------------------------------------
# Combined Update/Delete Block
#------------------------------------------------------------------------------------------------------------

@route('/test_Update_Delete', method = 'GET')
def show_all_items():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo")
    result = c.fetchall()             # fetches all items in Todo database and stores data in variable 'result'
    c.close()
    #print(result)
    unzippedResult = zip(*result)
    #for data in unzippedResult:
        #print (data)
    namesList = list(unzippedResult)
    for data in namesList:
        print(data)
    return template('Alternate_dropdown.tpl',rows=result) # sends result data to template to display all items in todo list and choose item to edit

@route('/test_Update_Delete', method = 'POST')   # returns delete item ID and stores in variable delete_id
def delete_item_found():
    returned_item = request.POST.get('tab','').strip()
    if returned_item[2] == ',':
        id = returned_item[1]
    else:
        id = returned_item[1] + returned_item[2]

    
    #return str(id)
    #redirect('/delete/{}'.format(delete_id))   # redirects to delete function passing delelte_id
    #delete_id = request.POST.get('todoID','').strip()
    redirect('/delete/{}'.format(id)) 

#------------------------------------------------------------------------------------------------------------
# Display Error Message - if Item does not Exist
#------------------------------------------------------------------------------------------------------------

@route('/invalid_item')
def Item_not_found():
    return template('item_not_found.tpl')


#------------------------------------------------------------------------------------------------------------
# Validation of item using regular expressions --- above edit item will raise exception when a float is entered ---
#------------------------------------------------------------------------------------------------------------
@route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    c.close()
    if not result:
        return 'This item number does not exist!'
    else:
        return 'Task: %s' % result[0]

#------------------------------------------------------------------------------------------------------------
# validation using RE and return a json object which can be referenced as a python dictionary
#------------------------------------------------------------------------------------------------------------
@route('/json<json:re:[0-9]+>')
def show_json(json):    
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()
    print(result)
    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


run() #host='0.0.0.0', port = 8080, reloader = True, debug = True)
