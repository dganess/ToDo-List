%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<h1>The open items are as follows:</h1>
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

<form action = "/" >
    <button type="submit"> Homepage</button>
</form>