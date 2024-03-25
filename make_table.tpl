%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<h1>The {{sample_text}} items are as follows:</h1>
<table border="5">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  <td>
    <form action = "/edit/{{row[0]}}" >
      <button type="submit">Edit</button>
    </form>
  </td>
  <td>
    <form action = "/delete/{{row[0]}}" >
      <button type="submit">Delete</button>
    </form>
  </td>
  </tr>

%end

</table>
   
<br>

<form action = "/" >
    <button type="submit"> Homepage</button>
</form>