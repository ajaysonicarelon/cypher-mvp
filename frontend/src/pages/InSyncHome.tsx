import React, { useEffect } from 'react';
import { ThemeProvider } from '@ajaysoni7832/lean-ids-components';
import { carelonTheme } from '@ajaysoni7832/lean-ids-tokens';
import './InSyncHome.css';

// Image URLs from Figma
const carelonInsyncLogo = "https://www.figma.com/api/mcp/asset/c9513b22-b43b-4488-be1c-22b61731eef8";
const profileImage = "https://www.figma.com/api/mcp/asset/95cbc5db-1281-4432-aa46-0f1939bd9d71";

interface ServiceCard {
  id: string;
  title: string;
  description: string;
  link: string;
}

const serviceCards: ServiceCard[] = [
  { id: '1', title: 'My HyWo compliance Details', description: 'My HyWo compliance Details', link: '#' },
  { id: '2', title: 'My Profile', description: 'My Profile', link: '#' },
  { id: '3', title: 'HyWo Exception', description: 'HyWo Exception', link: '#' },
  { id: '4', title: 'Relocation Request', description: 'Relocation Request', link: '#' },
  { id: '5', title: 'View SEZ Card', description: 'View SEZ Card', link: '#' },
  { id: '6', title: 'Infractions', description: 'Infractions', link: '#' },
];

function InSyncHome() {
  useEffect(() => {
    // Small delay to ensure DOM is ready
    const timer = setTimeout(() => {
      // Check if widget already exists
      const existingWidget = document.getElementById('cypher-chatbot-widget');
      if (existingWidget) {
        console.log('✅ Chatbot widget already exists');
        return;
      }

      // Load chatbot widget script
      console.log('📦 Loading chatbot widget script...');
      const script = document.createElement('script');
      script.src = '/insync-chatbot-widget.js';
      script.async = true;
      script.onload = () => {
        console.log('✅ Chatbot widget script loaded');
        // Give it a moment to initialize
        setTimeout(() => {
          const fab = document.getElementById('cypher-fab');
          const chatWindow = document.getElementById('cypher-chat-window');
          console.log('🔍 After load - FAB:', fab, 'Chat Window:', chatWindow);
        }, 100);
      };
      script.onerror = () => {
        console.error('❌ Failed to load chatbot widget script');
      };
      document.body.appendChild(script);
    }, 100);

    return () => {
      clearTimeout(timer);
      // Cleanup - remove widget but keep script for reuse
      const widget = document.getElementById('cypher-chatbot-widget');
      if (widget) {
        console.log('🧹 Cleaning up chatbot widget');
        widget.remove();
      }
    };
  }, []);

  return (
    <ThemeProvider theme={carelonTheme}>
      <div className="insync-page">
        {/* Main Content */}
        <main className="insync-main-full">
          <div className="insync-container">
            {/* What's New Section */}
            <section className="whats-new-section">
              <h2 className="section-title">What's New ?</h2>
              <div className="whats-new-card">
                <div className="whats-new-item">
                  <a href="#" className="whats-new-link">
                    My HyWo Compliance Details
                    <i className="fas fa-arrow-right"></i>
                  </a>
                </div>
                <div className="divider"></div>
                <div className="whats-new-item">
                  <a href="#" className="whats-new-link">
                    Back to School drive
                    <i className="fas fa-arrow-right"></i>
                  </a>
                </div>
                <div className="divider"></div>
                <div className="whats-new-item">
                  <p className="whats-new-text">
                    You can download the official Carelon Brand name change letter. Download
                    <button className="download-btn">
                      <i className="fas fa-download"></i>
                    </button>
                  </p>
                </div>
              </div>
            </section>

            {/* Content Grid */}
            <div className="content-grid">
              {/* Left Column - Service Catalog */}
              <div className="left-column">
                <div className="section-header">
                  <h2 className="section-title">Service Catalog</h2>
                  <button className="view-all-btn">
                    View All <i className="fas fa-arrow-right"></i>
                  </button>
                </div>
                
                <div className="service-grid">
                  {serviceCards.map((card) => (
                    <div key={card.id} className="service-card">
                      <a href={card.link} className="service-link">
                        {card.title}
                        <i className="fas fa-arrow-right"></i>
                      </a>
                      <div className="service-divider"></div>
                      <p className="service-description">{card.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Right Column */}
              <div className="right-column">
                {/* Profile Section */}
                <section className="profile-section">
                  <h2 className="section-title">Profile</h2>
                  <div className="profile-card">
                    <div className="profile-header">
                      <div className="profile-avatar">
                        <i className="fas fa-user"></i>
                      </div>
                      <div className="profile-info">
                        <p className="profile-name">., Ajay</p>
                        <p className="profile-role">Sr UX Designer II (IND)</p>
                        <p className="profile-product">Carelon MBM - Product</p>
                        <p className="profile-domain">Domain ID: AM07832</p>
                        <a href="#" className="profile-link">View Profile →</a>
                      </div>
                    </div>
                  </div>
                </section>

                {/* Notification Section */}
                <section className="notification-section">
                  <h2 className="section-title">Notification</h2>
                  <div className="notification-card">
                    <div className="notification-item">
                      <div className="notification-header">
                        <span className="notification-id">REQID - 23549 - Rejected</span>
                        <i className="fas fa-chevron-right"></i>
                      </div>
                      <p className="notification-text">HyWo Exception Till - 09/30/2024</p>
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </div>
        </main>

        {/* Chatbot Widget Script */}
        <div id="cypher-chatbot-mount"></div>
      </div>
    </ThemeProvider>
  );
}

export default InSyncHome;
