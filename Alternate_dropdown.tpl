<h1>Select Item to Update/Delete:</h1>   
     
     
<form action = "/test_Update_Delete" method = 'POST' >

    <label for="dtata">Choose an Item:</label>

    <select name="tab" id="list">
        %for row in rows:
            #%for col in row:
                <option value="{{row}}">{{row[0]}}</option>
            #%end
        %end
    </select>

    <input type="submit" name = 'save'>Update/Delete</button>
</form>