import React, { useEffect, useState } from "react";
function App() {
  const [Transaction, setTransaction] = useState([]);
  useEffect(() => {
    fetchTransaction();
  }, []);
  const fetchTransaction = async () => {
    try{
      const reponse = await fetch("http://127.0.0.1:8000/api/transaction/");
      const data = await reponse.json();
      console.log(data); 
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };
  return (
    <div className="App">
      <h1>Hello World</h1>
    </div>
  );
}

export default App;