import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

function FormulaireAjout() { // Renomme bien la fonction si c'est ta page ajout
    const [nom_td, setNom_td] = useState("");
    const [desc, setDesc] = useState("");
    const navigate = useNavigate();

    const handlesubmit = (e) => {
        e.preventDefault(); 
        
        axios.post("http://127.0.0.1:8000/api/api/todo/", {
            nom_todo: nom_td,      // Doit être identique au modèle Django
            description: desc
        })
        .then(res => {
            console.log('Ajout réussi', res.data);
            navigate("/"); // Redirige vers la liste après succès
        })
        .catch(err => {
            console.error("Erreur lors d'ajout: ", err);
            alert("Erreur lors de l'envoi");
        });
    };

    // LOGIQUE : Le return doit avoir des parenthèses () pour englober le HTML
    return (
        <div
            style={{
                maxWidth: '500px',
                margin: '56px auto',
                padding: '40px 32px',
                background: 'white',
                borderRadius: '22px',
                boxShadow: '0 8px 32px rgba(65,16,134,0.13)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
            }}
        >
            <h2 style={{
                background: 'linear-gradient(90deg,#7a40fc 0%,#21d4fd 70%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontSize: '2.2rem',
                fontWeight: 700,
                letterSpacing: '1px',
                marginBottom: '34px'
            }}>
                Ajouter une tâche
            </h2>
            <form
                onSubmit={handlesubmit}
                style={{
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '24px'
                }}
                autoComplete="off"
            >
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
                    }}
                />
                <button
                    type="submit"
                    style={{
                        padding: '16px',
                        border: 'none',
                        borderRadius: '12px',
                        fontWeight: 700,
                        fontSize: '1.15rem',
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
                    + Ajouter
                </button>
            </form>
        </div>
    );
}



export default FormulaireAjout;
