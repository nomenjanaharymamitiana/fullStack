import { useEffect, useState } from "react";
import { Link } from 'react-router-dom';
import axios from "axios";


function App() {
    const [item, setItem] = useState([]);
    const API_BASE_URL = "https://fullstack-4jgu.onrender.com/api/api/todo/";

    useEffect(() => {
        axios.get(API_BASE_URL)
             .then(res => setItem(res.data))
             .catch(err => console.log(err));
    }, []);
   // à mettre en haut du fichier (uniquement la première fois)

const supprimerTodo = (id) => {
    // Test simple avec la boîte de dialogue native du navigateur
    if (window.confirm("Voulez-vous vraiment supprimer cette tâche ?")) {
        
        // On s'assure que l'URL est : https://.../api/todo/ID/
        axios.delete(`${API_BASE_URL}${id}/`) 
            .then(() => {
                // Alerte de succès
                const alertDiv = document.createElement('div');
                alertDiv.className = "fixed top-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded shadow-lg z-50";
                alertDiv.innerText = "Tâche supprimée !";
                document.body.appendChild(alertDiv);
                setTimeout(() => alertDiv.remove(), 2000);

                // Mise à jour de l'état
                setItem(item.filter(todo => todo.id_todo !== id));
            })
            .catch(err => {
                console.error("Détails de l'erreur :", err.response);
                alert("Erreur lors de la suppression. Vérifiez la console.");
            });
    }
}

    return (
        <div
            style={{
                maxWidth: '600px',
                margin: '48px auto',
                background: '#fff',
                borderRadius: '18px',
                padding: '40px 32px',
                boxShadow: '0 10px 32px rgba(0,0,0,0.12)',
                minHeight: '80vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
            }}
        >
            <Link
                to="/ajouter"
                style={{
                    padding: '14px 32px',
                    background: 'linear-gradient(90deg,#21d4fd 0%,#b721ff 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '10px',
                    fontWeight: 700,
                    fontSize: '1.25rem',
                    marginBottom: '30px',
                    letterSpacing: '1px',
                    boxShadow: '0 4px 20px rgba(33,212,253,0.16)',
                    transition: 'transform 0.1s, box-shadow 0.2s',
                    cursor: 'pointer',
                    textDecoration: 'none',
                    outline: 'none',
                }}
                onMouseOver={e => {
                    e.target.style.transform = 'scale(1.05)';
                    e.target.style.boxShadow = '0 8px 40px rgba(183,33,255,0.22)';
                }}
                onMouseOut={e => {
                    e.target.style.transform = 'none';
                    e.target.style.boxShadow = '0 4px 20px rgba(33,212,253,0.16)';
                }}
            >
                + Ajouter une tâche
            </Link>
            <ul style={{
                width: '100%',
                marginTop: '14px',
                listStyle: 'none',
                padding: 0,
                display: 'grid',
                gap: '22px',
            }}>
                {item.map(todo => (
                    <li key={todo.id_todo}
                        style={{
                            padding: '24px',
                            borderRadius: '14px',
                            background: 'linear-gradient(90deg,#ece9f7 60%,#f7fafd 100%)',
                            boxShadow: '0 2px 10px rgba(76, 90, 151, 0.10)',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '7px',
                        }}
                    >
                        <span style={{
                            fontWeight: 600,
                            fontSize: '1.15rem',
                            color: '#7a40fc',
                        }}>
                            Tâche #{todo.id_todo}
                        </span>
                        <span style={{
                            fontSize: '1.05rem',
                            color: '#353046',
                            fontWeight: 500
                        }}>
                            {todo.nom_todo}
                        </span>
                        <span style={{
                            color: '#6d7281',
                            fontSize: '1rem'
                        }}>
                            {todo.description}
                        </span>
                        <span>
                            <span style={{ fontSize: '0.88rem', color: '#8b8b97', fontStyle: 'italic' }}>
                                {todo.dateCreate ? new Date(todo.dateCreate).toLocaleString('fr-FR', { 
                                    day: '2-digit', 
                                    month: 'long', 
                                    year: 'numeric', 
                                    hour: '2-digit', 
                                    minute: '2-digit'
                                }) : ''}
                            </span>
                        </span>
                        <button 
                            onClick={() => supprimerTodo(todo.id_todo)} 
                            style={{ color: 'red', cursor: 'pointer' }}
                        >
                            <span style={{
                                fontWeight: 600,
                                color: 'red',
                                letterSpacing: '1px',
                                fontSize: '1.1rem',
                                display: 'inline-block',
                                padding: '7px 20px',
                                borderRadius: '9px',
                                background: 'linear-gradient(90deg,#ffe4e4 0%,#fff0f0 75%)',
                                border: 'none',
                                boxShadow: '0 1px 6px rgba(234,45,85,0.13)',
                                cursor: 'pointer',
                                transition: 'background 0.17s, color 0.15s'
                            }}>
                                Supprimer
                            </span>
                        </button>
                        <Link 
                            to={`/modifier_todo/${todo.id_todo}`} 
                            style={{
                                color: '#2196f3',
                                textDecoration: 'none',
                                fontWeight: 600,
                                marginTop: '6px',
                                padding: '7px 18px',
                                borderRadius: '9px',
                                background: 'linear-gradient(90deg,#e3f0ff 0%,#e9e7fc 70%)',
                                transition: 'background 0.2s, color 0.2s',
                                display: 'inline-block',
                            }}
                            onMouseOver={e => {
                                e.target.style.background = 'linear-gradient(90deg,#b721ff 0%,#21d4fd 100%)';
                                e.target.style.color = '#fff';
                            }}
                            onMouseOut={e => {
                                e.target.style.background = 'linear-gradient(90deg,#e3f0ff 0%,#e9e7fc 70%)';
                                e.target.style.color = '#2196f3';
                            }}
                        >
                            Modifier
                        </Link>
                        
                    </li>
                ))}
            </ul>
        </div>
    );
}
export default App;
// Amélioration du design moderne avec un bouton "Ajouter" plus visible et une liste stylisée

/* Si vous avez Tailwind CSS disponible, ces classes donneront un design épuré et moderne.
   Sinon, remplacez les classes par votre framework CSS préféré ou des styles basiques. */

//
// 1. Pour améliorer l'apparence du bouton et la mise en page :
//
// - Centrer la liste et le bouton
// - Donner du padding, background blanc, ombre et coins arrondis au conteneur
// - Le bouton "Ajouter" est large, coloré et possède un effet de survol moderne
// - Les items sont disposés joliment avec une grille responsive
//
// → VOUS POUVEZ déplacer ce bloc dans `return` si besoin, ici ça illustre juste comment styliser.
//

// Pas de code à ajouter ici. Tout est déjà intégré dans le composant.
// Tout est géré par les classes Tailwind CSS dans le rendu existant des boutons et des items.
// Pour des améliorations supplémentaires, voici un exemple de styles "inline" si vous ne souhaitez pas utiliser de framework :





// Pour utiliser Tailwind : assurez-vous qu'il est bien installé et gardez votre code tel quel,
// il bénéficiera déjà d'un design moderne !
