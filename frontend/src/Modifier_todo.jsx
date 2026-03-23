import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate , useParams } from "react-router-dom";


function Modifier_todo(){
    const {id}= useParams();
    const navigate = useNavigate();
    const [nom_td, setNom_td]= useState("")
    const [desc,setDesc]=useState("")
   // Option A : Modifie la constante (recommandé)
const API_BASE_URL = "https://fullstack-4jgu.onrender.com/api/api/todo/"; // Pas de / à la fin

// Option B : Modifie l'appel (si tu gardes le / dans la constante)
useEffect(() => {
    // On enlève le / entre BASE_URL et id car il est déjà dans la constante
    axios.get(`${API_BASE_URL}${id}/`).then(res => { 
        setNom_td(res.data.nom_todo);
        setDesc(res.data.description);
    }).catch(error => console.error("Erreur :", error));
}, [id, API_BASE_URL]);

    const handleupdate =(e)=>{
        e.preventDefault();
        axios.put(`${API_BASE_URL}${id}/`,{
            nom_todo : nom_td,
            description : desc
     }).then(()=>{
        alert("Modifier avec succes");
        navigate("/");
        
    }).catch(err => console.error("errruer lors de la modification :" , err))
    }
    return(
        <form onSubmit={handleupdate} style={{
            maxWidth: '500px',
            margin: '56px auto',
            padding: '40px 32px',
            background: 'white',
            borderRadius: '22px',
            boxShadow: '0 8px 32px rgba(65,16,134,0.13)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
        }}>
            <h2 style={{
                background: 'linear-gradient(90deg,#7a40fc 0%,#21d4fd 70%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontSize: '2.2rem',
                fontWeight: 700,
                letterSpacing: '1px',
                marginBottom: '34px'
            }}>
                Modifier la tâche
            </h2>
            <input
                type="text"
                value={nom_td}
                onChange={e => setNom_td(e.target.value)}
                placeholder="Nom de la todo"
                required
                style={{
                    padding: '16px 18px',
                    border: 'none',
                    borderRadius: '10px',
                    boxShadow: '0 2px 12px rgba(122,64,252,0.07)',
                    fontSize: '1.15rem',
                    background: '#f7f7fa',
                    outline: 'none',
                    fontWeight: 500,
                    transition: 'box-shadow 0.2s',
                    marginBottom: '22px',
                    width: '100%',
                }}
            />
            <input
                type="text"
                value={desc}
                onChange={e => setDesc(e.target.value)}
                placeholder="Description"
                required
                style={{
                    padding: '16px 18px',
                    border: 'none',
                    borderRadius: '10px',
                    boxShadow: '0 2px 12px rgba(122,64,252,0.07)',
                    fontSize: '1.1rem',
                    background: '#f7f7fa',
                    outline: 'none',
                    fontWeight: 500,
                    transition: 'box-shadow 0.2s',
                    marginBottom: '24px',
                    width: '100%',
                }}
            />
            <div style={{display: 'flex', width: '100%', gap: '16px'}}>
                <button
                    type="submit"
                    style={{
                        flex: 1,
                        padding: '16px',
                        border: 'none',
                        borderRadius: '12px',
                        fontWeight: 700,
                        fontSize: '1.1rem',
                        background: 'linear-gradient(90deg,#21d4fd 0%,#b721ff 100%)',
                        color: '#fff',
                        letterSpacing: '1.1px',
                        cursor: 'pointer',
                        boxShadow: '0 4px 24px rgba(42,163,255,0.13)',
                        transition: 'transform 0.1s, box-shadow 0.18s',
                    }}
                    onMouseOver={e => {
                        e.target.style.transform = 'scale(1.04)';
                        e.target.style.boxShadow = '0 8px 32px rgba(33,212,253,0.14)';
                    }}
                    onMouseOut={e => {
                        e.target.style.transform = 'none';
                        e.target.style.boxShadow = '0 4px 24px rgba(42,163,255,0.13)';
                    }}
                >
                    Appliquer
                </button>
                <button
                    type="reset"
                    style={{
                        flex: 1,
                        padding: '16px',
                        border: 'none',
                        borderRadius: '12px',
                        fontWeight: 700,
                        fontSize: '1.1rem',
                        background: 'linear-gradient(90deg,#ffcfd2 0%,#ff8783 100%)',
                        color: '#a10000',
                        letterSpacing: '1.1px',
                        cursor: 'pointer',
                        boxShadow: '0 4px 24px rgba(255,140,140,0.13)',
                        transition: 'transform 0.1s, box-shadow 0.18s',
                    }}
                    onMouseOver={e => {
                        e.target.style.transform = 'scale(1.04)';
                        e.target.style.boxShadow = '0 8px 32px rgba(255,66,66,0.10)';
                    }}
                    onMouseOut={e => {
                        e.target.style.transform = 'none';
                        e.target.style.boxShadow = '0 4px 24px rgba(255,140,140,0.13)';
                    }}
                >
                    Annuler
                </button>
            </div>
        </form>
    )
}
export default Modifier_todo;  
  
