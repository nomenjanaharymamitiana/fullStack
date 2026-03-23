import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './nav_bar';
import Listtodo from './Listtodo';
import FormulaireAjout from './FormulaireAjout';
import Modifier_todo from './Modifier_todo'

function App() {
  return (
    <BrowserRouter>
 

      <Routes>
        {/* 2. Page d'accueil (Liste) */}
        <Route path="/" element={<Listtodo/>} />
        <Route path="/modifier_todo/:id" element={<Modifier_todo />} />

        
        {/* 3. Page d'ajout (Chemin différent !) */}
        <Route path="/ajouter" element={<FormulaireAjout/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
