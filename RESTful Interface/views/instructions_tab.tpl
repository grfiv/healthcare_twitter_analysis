      
      <p>These instructions assume the following:</p>
      <ul>
        <li>you have created a MongoDB database as follows<br>
         <span style='font-family:"Courier New"'>mongoimport -d HTA -c grf --file HTA_noduplicates.json</span><br>
         on an external hard drive, location <span style='font-family:"Courier New"'>E:\HTA</span><br>
         (the status report on the repo ... <a href="https://github.com/grfiv/healthcare_twitter_analysis">HTA repo</a>
         ... has detailed instructions).</li><br>
         
        <li>you have this webpage, <span style='font-family:"Courier New"'>HTAinterface.html</span> 
          and the Bottle Server, <span style='font-family:"Courier New"'>bottle_server.py</span><br>
          on the same external hard drive in location <span style='font-family:"Courier New"'>E:\HTA\RESTful Interface</span><br>
          with the supporting files in the structure shown in the repo.</li><br>
          
        <li>you are using the latest version of the Chrome browser; others may work, but only by luck.</li>
      </ul>
          
      <p>Obviously, these instructions apply to a Windows machine; Linux and Mac folks will have to adapt.</p>
        
      <ol>
        <li>Start the MongoDB Server using the database on the external drive<br>
          <ol>
            <li>Start a command window as Administrator</li>
            <li><span style='font-family:"Courier New"'>net stop MongoDB</span></li>
            <li><span style='font-family:"Courier New"'>mongod --dbpath "E:\HTA"</span></li>
          </ol>
        </li><br>
        
        <li>Start the Bottle HTTP Server<br>
          <ol>
            <li>Start another command window</li>
            <li><span style='font-family:"Courier New"'>e:</span></li>
            <li><span style='font-family:"Courier New"'>cd E:\HTA\RESTful Interface</span></li>
            <li><span style='font-family:"Courier New"'>python bottle_server.py</span></li>
          </ol>
        </li><br>
        
        <li>Using Chrome, load the interface web page<br>
          <span style='font-family:"Courier New"'>http://localhost:8082/</span>
        </li>
      </ol>
      
      <p>The interface is very simple: there are only two things you have to enter ...</p>
      <ul>
        <li>A MongoDB query in exactly the format used on the mongo command line</li>
        <li>A limit on the number of documents to return; set to zero (0) and the '_id's of all the matching documents will be returned</li>
      </ul>
      
      <p>At the moment you only see displayed the result of the query:</p>
      <ul>
        <li>a list of the '_id's that match, up to the limit ("id_list")</li>
        <li>the number in that list ("num")</li>
        <li>the first matching document ("example")</li>
      </ul>
      
      <p>My expectation is to enhance this system so that you can scroll through all the matching documents; 
         the plan is to make ajax requests behind the scenes as you scroll through so that an entire mass of data isn't sent down all at once, 
         storing the documents received so far in Chrome's IndexedDB local storage facility for quick random-access retrieval.</p>
         