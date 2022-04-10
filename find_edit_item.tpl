%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<h1>All items are as follows:</h1>
<table border="5">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>

<br>

 <head>
    <title>Welcome to my ToDo Edit Query</title>
  </head>
  <body>
    

%# edit item number returned to /find_item POST method function
<form action = "/find_item" method="POST" >                     
    <label for="no">What numbered item would you like to edit?>
    <input name="todoID" type ="number">
    <input type="submit" name = "save"value = "Query">
</form>



<form action = "/" >
    <button type="submit"> Homepage</button>
</form>
