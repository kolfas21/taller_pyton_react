import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function SelectDesdeLista() {
  const [opciones, setOpciones] = useState([]);
  const [seleccionado, setSeleccionado] = useState('');
  const [gifUrl, setGifUrl] = useState('');
  const [cargando, setCargando] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:8000/paises')
      .then((response) => {
        setOpciones(response.data);
      })
      .catch((error) => {
        console.error('Error al obtener los datos:', error);
      });
  }, []);

  const manejarCambio = async (event) => {
    const valor = event.target.value;
    setSeleccionado(valor);
    setGifUrl('');
    setCargando(true);

    try {
      await axios.get(`http://localhost:8000/pais/${valor}`);
      // Asumimos que al volver del backend, el GIF ya se generó
      const urlGif = `http://localhost:8000/animaciones/${valor}_renewables.gif`;
      setGifUrl(urlGif);
    } catch (error) {
      console.error('Error al obtener el detalle:', error);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div>
      <label htmlFor="pais">Selecciona un país:</label>
      <select id="pais" value={seleccionado} onChange={manejarCambio}>
        <option value="">-- Selecciona una opción --</option>
        {opciones.map((opcion, index) => (
          <option key={index} value={opcion}>
            {opcion}
          </option>
        ))}
      </select>

      {cargando && <p>Generando gráfico...</p>}

      {gifUrl && (
        <div style={{ marginTop: '1rem' }}>
          <img
            src={gifUrl}
            alt={'GIF de ${seleccionado}'}
            style={{ maxWidth: '100%', border: '1px solid #ccc' }}
          />
        </div>
      )}
    </div>
  );
}