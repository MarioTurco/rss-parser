import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# Configurazione DB (adatta ai tuoi parametri)
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'airflow'),
    'user': os.getenv('POSTGRES_USER', 'airflow'),
    'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
    'port': int(os.getenv('POSTGRES_PORT', 5432))
}

def get_rss_items():
    """
    Qui metti la tua logica per estrarre gli items dal DB.
    Per ora, restituisce elementi finti per testare l'UI.
    """
    # Dati finti per testare l'interfaccia
    fake_items = [
        {
            'title': 'Titolo Articolo 1',
            'description': 'Questa è una descrizione finta del primo articolo RSS.',
            'author': 'Autore 1',
            'source': 'Fonte 1',
            'link': 'https://example.com/article1',
            'pub_date': '2026-03-29 10:00:00'
        },
        {
            'title': 'Titolo Articolo 2',
            'description': 'Questa è una descrizione finta del secondo articolo RSS.',
            'author': 'Autore 2',
            'source': 'Fonte 2',
            'link': 'https://example.com/article2',
            'pub_date': '2026-03-28 15:30:00'
        },
        {
            'title': 'Titolo Articolo 3',
            'description': 'Questa è una descrizione finta del terzo articolo RSS.',
            'author': 'Autore 3',
            'source': 'Fonte 3',
            'link': 'https://example.com/article3',
            'pub_date': '2026-03-27 09:15:00'
        },
        {
            'title': 'Titolo Articolo 4',
            'description': 'Questa è una descrizione finta del quarto articolo RSS.',
            'author': 'Autore 4',
            'source': 'Fonte 4',
            'link': 'https://example.com/article4',
            'pub_date': '2026-03-26 14:45:00'
        }
    ]
    return fake_items

def main():
    # Sidebar con pulsanti cliccabili
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Feed"
    
    with st.sidebar:
        st.title("Menu")
        
        if st.button("📡 Feed", use_container_width=True, 
                    type="primary" if st.session_state.current_page == "Feed" else "secondary"):
            st.session_state.current_page = "Feed"
        
        if st.button("⚙️ Gestisci Feed", use_container_width=True,
                    type="primary" if st.session_state.current_page == "Gestisci Feed" else "secondary"):
            st.session_state.current_page = "Gestisci Feed"
    
    if st.session_state.current_page == "Feed":
        st.title("📰 RSS Feed Reader")
        
        items = get_rss_items()
        
        if not items:
            st.info("Nessun articolo trovato. Aggiungi alcuni feed RSS per iniziare!")
            return
        
        # Filtri e controlli
        st.markdown("### Filtri e Ricerca")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Filtro per fonte
            sources = list(set(item['source'] for item in items if item['source']))
            sources.insert(0, "Tutte le fonti")
            selected_source = st.selectbox("Fonte", sources)
        
        with col2:
            # Filtro per autore
            authors = list(set(item['author'] for item in items if item['author']))
            authors.insert(0, "Tutti gli autori")
            selected_author = st.selectbox("Autore", authors)
        
        with col3:
            # Filtro per data
            date_options = ["Tutte le date", "Oggi", "Ultimi 3 giorni", "Ultima settimana", "Ultimo mese"]
            selected_date_filter = st.selectbox("Periodo", date_options)
        
        with col4:
            # Numero di articoli per pagina
            items_per_page = st.selectbox("Per pagina", [5, 10, 20, 50], index=1)
        
        # Applica filtri
        filtered_items = items.copy()
        
        if selected_source != "Tutte le fonti":
            filtered_items = [item for item in filtered_items if item['source'] == selected_source]
        
        if selected_author != "Tutti gli autori":
            filtered_items = [item for item in filtered_items if item['author'] == selected_author]
        
        # Filtro data semplice (basato su stringhe)
        if selected_date_filter != "Tutte le date":
            from datetime import datetime, timedelta
            now = datetime.now()
            
            if selected_date_filter == "Oggi":
                cutoff = now - timedelta(days=1)
            elif selected_date_filter == "Ultimi 3 giorni":
                cutoff = now - timedelta(days=3)
            elif selected_date_filter == "Ultima settimana":
                cutoff = now - timedelta(days=7)
            else:  # Ultimo mese
                cutoff = now - timedelta(days=30)
            
            filtered_items = [item for item in filtered_items if 
                            datetime.strptime(item['pub_date'], '%Y-%m-%d %H:%M:%S') > cutoff]
        
        # Paginazione
        total_items = len(filtered_items)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        
        if 'current_page_num' not in st.session_state:
            st.session_state.current_page_num = 1
        
        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("◀ Precedente") and st.session_state.current_page_num > 1:
                    st.session_state.current_page_num -= 1
            with col2:
                st.write(f"Pagina {st.session_state.current_page_num} di {total_pages}")
            with col3:
                if st.button("Successivo ▶") and st.session_state.current_page_num < total_pages:
                    st.session_state.current_page_num += 1
        else:
            st.session_state.current_page_num = 1
        
        # Mostra articoli della pagina corrente
        start_idx = (st.session_state.current_page_num - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_items = filtered_items[start_idx:end_idx]
        
        st.markdown(f"### Articoli ({total_items} totali)")
        
        # Mostra come cards Reddit-like compatte
        for item in page_items:
            with st.container():
                # Layout compatto: thumbnail piccolo + contenuto
                col_thumb, col_content = st.columns([0.8, 4])
                
                with col_thumb:
                    # Thumbnail più piccolo e compatto
                    st.markdown("""
                    <div style="
                        width: 40px;
                        height: 40px;
                        background-color: #f8f9fa;
                        border-radius: 3px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 1px solid #e9ecef;
                        font-size: 14px;
                    ">
                        📰
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_content:
                    # Titolo più piccolo
                    st.markdown(f"**[{item['title']}]({item['link']})**", help=None)
                    
                    # Meta informazioni compatte
                    meta_parts = []
                    if item['source']:
                        meta_parts.append(f"📰 {item['source']}")
                    if item['author']:
                        meta_parts.append(f"👤 {item['author']}")
                    if item['pub_date']:
                        # Formatta data in modo più compatto
                        try:
                            from datetime import datetime
                            dt = datetime.strptime(item['pub_date'], '%Y-%m-%d %H:%M:%S')
                            meta_parts.append(f"📅 {dt.strftime('%d/%m %H:%M')}")
                        except:
                            meta_parts.append(f"📅 {item['pub_date']}")
                    
                    if meta_parts:
                        st.caption(" • ".join(meta_parts))
                    
                    # Descrizione più corta e compatta
                    if item['description']:
                        desc = item['description'][:120] + "..." if len(item['description']) > 120 else item['description']
                        st.caption(desc)
                
                # Separatore sottile
                st.markdown('<hr style="margin: 8px 0; border: none; border-top: 1px solid #f0f0f0;">', unsafe_allow_html=True)
                
    elif st.session_state.current_page == "Gestisci Feed":
        st.title("⚙️ Gestisci Feed RSS")
        st.markdown("### Aggiungi o Rimuovi Feed")
        st.info("Funzionalità in sviluppo. Qui potrai gestire i tuoi feed RSS preferiti.")
        
        # Placeholder per future funzionalità
        with st.expander("Feed Attivi"):
            st.write("• Feed di esempio 1")
            st.write("• Feed di esempio 2")
        
        with st.expander("Aggiungi Nuovo Feed"):
            url = st.text_input("URL del Feed RSS")
            nome = st.text_input("Nome del Feed")
            if st.button("Aggiungi Feed"):
                st.success(f"Feed '{nome}' aggiunto! (simulato)")

if __name__ == "__main__":
    main()
