import React, { useState } from 'react';
import { 
  Button, 
  Chip, 
  Icon,
  MetricCard
} from '@ajaysoni7832/lean-ids-components';

interface Product {
  id: string;
  name: string;
  domain: string;
  widgets: number;
  active: boolean;
}

interface Widget {
  id: string;
  name: string;
  productId: string;
  apiKey: string;
  active: boolean;
}

const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'products' | 'widgets' | 'knowledge' | 'analytics'>('products');
  
  const [products, setProducts] = useState<Product[]>([
    { id: '1', name: 'InSync', domain: 'insync.carelon.com', widgets: 1, active: true },
  ]);

  const [widgets, setWidgets] = useState<Widget[]>([
    { id: '1', name: 'InSync Chatbot', productId: '1', apiKey: 'demo-key', active: true },
  ]);

  const [knowledgeItems, setKnowledgeItems] = useState<any[]>([
    { id: '1', question: 'What is HyWo?', answer: 'HyWo stands for Hybrid Work...', category: 'Onboarding' },
    { id: '2', question: 'How do I submit a HyWo Exception?', answer: 'Submit through the HR portal...', category: 'Onboarding' },
  ]);

  const [showProductModal, setShowProductModal] = useState(false);
  const [showWidgetModal, setShowWidgetModal] = useState(false);
  const [showKnowledgeModal, setShowKnowledgeModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [editingWidget, setEditingWidget] = useState<Widget | null>(null);
  const [editingKnowledge, setEditingKnowledge] = useState<any>(null);

  const stats = {
    products: products.length,
    widgets: widgets.length,
    knowledgeItems: knowledgeItems.length,
    messagesThisMonth: 1200,
  };

  // Product CRUD functions
  const handleAddProduct = () => {
    setEditingProduct(null);
    setShowProductModal(true);
  };

  const handleEditProduct = (product: Product) => {
    setEditingProduct(product);
    setShowProductModal(true);
  };

  const handleDeleteProduct = (id: string) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      setProducts(products.filter(p => p.id !== id));
    }
  };

  const handleSaveProduct = (productData: Omit<Product, 'id'>) => {
    if (editingProduct) {
      setProducts(products.map(p => p.id === editingProduct.id ? { ...editingProduct, ...productData } : p));
    } else {
      const newProduct = { ...productData, id: Date.now().toString(), widgets: 0 };
      setProducts([...products, newProduct]);
    }
    setShowProductModal(false);
    setEditingProduct(null);
  };

  // Widget CRUD functions
  const handleAddWidget = () => {
    setEditingWidget(null);
    setShowWidgetModal(true);
  };

  const generateApiKey = () => {
    return `cypher_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const handleEditWidget = (widget: Widget) => {
    setEditingWidget(widget);
    setShowWidgetModal(true);
  };

  const handleDeleteWidget = (id: string) => {
    if (window.confirm('Are you sure you want to delete this widget?')) {
      setWidgets(widgets.filter(w => w.id !== id));
    }
  };

  const handleSaveWidget = (widgetData: Omit<Widget, 'id'>) => {
    if (editingWidget) {
      setWidgets(widgets.map(w => w.id === editingWidget.id ? { ...editingWidget, ...widgetData } : w));
    } else {
      const newWidget = { ...widgetData, id: Date.now().toString() };
      setWidgets([...widgets, newWidget]);
    }
    setShowWidgetModal(false);
    setEditingWidget(null);
  };

  // Knowledge Base CRUD functions
  const handleAddKnowledge = () => {
    setEditingKnowledge(null);
    setShowKnowledgeModal(true);
  };

  const handleEditKnowledge = (item: any) => {
    setEditingKnowledge(item);
    setShowKnowledgeModal(true);
  };

  const handleDeleteKnowledge = (id: string) => {
    if (window.confirm('Are you sure you want to delete this knowledge item?')) {
      setKnowledgeItems(knowledgeItems.filter(k => k.id !== id));
    }
  };

  const handleSaveKnowledge = (knowledgeData: any) => {
    if (editingKnowledge) {
      setKnowledgeItems(knowledgeItems.map(k => k.id === editingKnowledge.id ? { ...editingKnowledge, ...knowledgeData } : k));
    } else {
      const newKnowledge = { ...knowledgeData, id: Date.now().toString() };
      setKnowledgeItems([...knowledgeItems, newKnowledge]);
    }
    setShowKnowledgeModal(false);
    setEditingKnowledge(null);
  };

  return (
    <div style={{ padding: '24px' }}>
      <h2 style={{ marginBottom: '8px' }}>Dashboard</h2>
      <p style={{ color: '#666', marginBottom: '24px' }}>Manage your Cypher chatbot widgets</p>

      {/* Tab Navigation */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', borderBottom: '1px solid #e0e0e0', paddingBottom: '16px' }}>
        <Button
          variant={activeTab === 'products' ? 'primary' : 'secondary'}
          size="small"
          onClick={() => setActiveTab('products')}
        >
          Products
        </Button>
        <Button
          variant={activeTab === 'widgets' ? 'primary' : 'secondary'}
          size="small"
          onClick={() => setActiveTab('widgets')}
        >
          Widgets
        </Button>
        <Button
          variant={activeTab === 'knowledge' ? 'primary' : 'secondary'}
          size="small"
          onClick={() => setActiveTab('knowledge')}
        >
          Knowledge Base
        </Button>
        <Button
          variant={activeTab === 'analytics' ? 'primary' : 'secondary'}
          size="small"
          onClick={() => setActiveTab('analytics')}
        >
          Analytics
        </Button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <MetricCard value={stats.products} />
        <MetricCard value={stats.widgets} />
        <MetricCard value={stats.knowledgeItems} />
        <MetricCard value={stats.messagesThisMonth.toLocaleString()} />
      </div>

      {/* Products List */}
      {activeTab === 'products' && (
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '16px', borderBottom: '1px solid #e0e0e0' }}>
            <h3 style={{ margin: 0 }}>Products</h3>
            <Button variant="primary" size="small" leadingIcon={<Icon name="add" size="medium" />} onClick={handleAddProduct}>
              Add Product
            </Button>
          </div>
          {products.map((product) => (
            <div key={product.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', borderBottom: '1px solid #f0f0f0' }}>
              <div>
                <div style={{ fontWeight: '600' }}>{product.name}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>{product.domain}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <Chip label={`${product.widgets} widget`} type="default" variant="outlined" />
                <Chip label={product.active ? 'Active' : 'Inactive'} type={product.active ? 'success' : 'neutral'} variant="filled" />
                <Button variant="secondary" size="small" onClick={() => handleEditProduct(product)}>Edit</Button>
                <Button variant="secondary" size="small" onClick={() => handleDeleteProduct(product.id)}>Delete</Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Widgets List */}
      {activeTab === 'widgets' && (
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '16px', borderBottom: '1px solid #e0e0e0' }}>
            <h3 style={{ margin: 0 }}>Widgets</h3>
            <Button variant="primary" size="small" leadingIcon={<Icon name="add" size="medium" />} onClick={handleAddWidget}>
              Add Widget
            </Button>
          </div>
          {widgets.map((widget) => (
            <div key={widget.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', borderBottom: '1px solid #f0f0f0' }}>
              <div>
                <div style={{ fontWeight: '600' }}>{widget.name}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>API Key: {widget.apiKey}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <Chip label={widget.active ? 'Active' : 'Inactive'} type={widget.active ? 'success' : 'neutral'} variant="filled" />
                <Button variant="secondary" size="small" onClick={() => handleEditWidget(widget)}>Edit</Button>
                <Button variant="secondary" size="small" onClick={() => handleDeleteWidget(widget.id)}>Delete</Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Knowledge Base */}
      {activeTab === 'knowledge' && (
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '16px', borderBottom: '1px solid #e0e0e0' }}>
            <h3 style={{ margin: 0 }}>Knowledge Base</h3>
            <Button variant="primary" size="small" leadingIcon={<Icon name="add" size="medium" />} onClick={handleAddKnowledge}>
              Add Q&A
            </Button>
          </div>
          {knowledgeItems.map((item) => (
            <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', borderBottom: '1px solid #f0f0f0' }}>
              <div>
                <div style={{ fontWeight: '600' }}>{item.question}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>{item.category}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <Button variant="secondary" size="small" onClick={() => handleEditKnowledge(item)}>Edit</Button>
                <Button variant="secondary" size="small" onClick={() => handleDeleteKnowledge(item.id)}>Delete</Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Analytics */}
      {activeTab === 'analytics' && (
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '16px', borderBottom: '1px solid #e0e0e0' }}>
            <h3 style={{ margin: 0 }}>Analytics</h3>
          </div>
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <p>Analytics dashboard coming soon</p>
          </div>
        </div>
      )}

      {/* Product Modal */}
      {showProductModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '8px', width: '400px', maxWidth: '90%' }}>
            <h3 style={{ marginBottom: '16px' }}>{editingProduct ? 'Edit Product' : 'Add Product'}</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Name</label>
              <input
                type="text"
                defaultValue={editingProduct?.name || ''}
                id="productName"
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Domain</label>
              <input
                type="text"
                defaultValue={editingProduct?.domain || ''}
                id="productDomain"
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Active</label>
              <input
                type="checkbox"
                defaultChecked={editingProduct?.active ?? true}
                id="productActive"
              />
            </div>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <Button variant="secondary" size="small" onClick={() => setShowProductModal(false)}>Cancel</Button>
              <Button
                variant="primary"
                size="small"
                onClick={() => {
                  const name = (document.getElementById('productName') as HTMLInputElement).value;
                  const domain = (document.getElementById('productDomain') as HTMLInputElement).value;
                  const active = (document.getElementById('productActive') as HTMLInputElement).checked;
                  handleSaveProduct({ name, domain, active, widgets: editingProduct?.widgets || 0 });
                }}
              >
                Save
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Widget Modal */}
      {showWidgetModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '8px', width: '400px', maxWidth: '90%' }}>
            <h3 style={{ marginBottom: '16px' }}>{editingWidget ? 'Edit Widget' : 'Add Widget'}</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Name</label>
              <input
                type="text"
                defaultValue={editingWidget?.name || ''}
                id="widgetName"
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Product</label>
              <select
                id="widgetProduct"
                defaultValue={editingWidget?.productId || products[0]?.id}
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              >
                {products.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
              </select>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>API Key</label>
              <div style={{ display: 'flex', gap: '8px' }}>
                <input
                  type="text"
                  defaultValue={editingWidget?.apiKey || generateApiKey()}
                  id="widgetApiKey"
                  style={{ flex: 1, padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
                />
                <Button variant="secondary" size="small" onClick={() => {
                  (document.getElementById('widgetApiKey') as HTMLInputElement).value = generateApiKey();
                }}>
                  Generate
                </Button>
              </div>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Active</label>
              <input
                type="checkbox"
                defaultChecked={editingWidget?.active ?? true}
                id="widgetActive"
              />
            </div>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <Button variant="secondary" size="small" onClick={() => setShowWidgetModal(false)}>Cancel</Button>
              <Button
                variant="primary"
                size="small"
                onClick={() => {
                  const name = (document.getElementById('widgetName') as HTMLInputElement).value;
                  const productId = (document.getElementById('widgetProduct') as HTMLSelectElement).value;
                  const apiKey = (document.getElementById('widgetApiKey') as HTMLInputElement).value;
                  const active = (document.getElementById('widgetActive') as HTMLInputElement).checked;
                  handleSaveWidget({ name, productId, apiKey, active });
                }}
              >
                Save
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Knowledge Modal */}
      {showKnowledgeModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '8px', width: '500px', maxWidth: '90%' }}>
            <h3 style={{ marginBottom: '16px' }}>{editingKnowledge ? 'Edit Q&A' : 'Add Q&A'}</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Question</label>
              <input
                type="text"
                defaultValue={editingKnowledge?.question || ''}
                id="knowledgeQuestion"
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Answer</label>
              <textarea
                defaultValue={editingKnowledge?.answer || ''}
                id="knowledgeAnswer"
                rows={4}
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Category</label>
              <input
                type="text"
                defaultValue={editingKnowledge?.category || ''}
                id="knowledgeCategory"
                style={{ width: '100%', padding: '8px', border: '1px solid #e0e0e0', borderRadius: '4px' }}
              />
            </div>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <Button variant="secondary" size="small" onClick={() => setShowKnowledgeModal(false)}>Cancel</Button>
              <Button
                variant="primary"
                size="small"
                onClick={() => {
                  const question = (document.getElementById('knowledgeQuestion') as HTMLInputElement).value;
                  const answer = (document.getElementById('knowledgeAnswer') as HTMLTextAreaElement).value;
                  const category = (document.getElementById('knowledgeCategory') as HTMLInputElement).value;
                  handleSaveKnowledge({ question, answer, category });
                }}
              >
                Save
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
