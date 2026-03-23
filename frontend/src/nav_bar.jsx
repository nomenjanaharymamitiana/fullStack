import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ 
      padding: '10px', 
      background: '#282c34', 
      color: 'white',
      display: 'flex',
      gap: '20px' 
    }}>
      {/* Liens de navigation */}
      <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
        🏠 Accueil (Liste)
      </Link>
      
      <Link to="/ajouter" style={{ color: 'white', textDecoration: 'none' }}>
        ➕ Ajouter une tâche
      </Link>
    </nav>
  );
}
export default Navbar;
