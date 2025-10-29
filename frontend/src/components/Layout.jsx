import React, { useState } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { 
  LayoutDashboard, 
  Package, 
  Users, 
  ShoppingCart, 
  Truck,
  ShoppingBag,
  Wrench,
  Tag,
  FileText,
  Headphones,
  BarChart3,
  Settings,
  Menu, 
  X,
  LogOut
} from 'lucide-react'

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user, logout } = useAuth()
  const location = useLocation()

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Produtos', href: '/produtos', icon: Package },
    { name: 'Clientes', href: '/clientes', icon: Users },
    { name: 'Vendas', href: '/vendas', icon: ShoppingCart },
    { name: 'Fornecedores', href: '/fornecedores', icon: Truck },
    { name: 'Compras', href: '/compras', icon: ShoppingBag },
    { name: 'Produtos Auxiliares', href: '/produtos-auxiliares', icon: Wrench },
    { name: 'Cupons', href: '/cupons', icon: Tag },
    { name: 'Notas Fiscais', href: '/notas-fiscais', icon: FileText },
    { name: 'Suporte', href: '/suporte', icon: Headphones },
    { name: 'Relatórios', href: '/relatorios', icon: BarChart3 },
    { name: 'Configurações', href: '/configuracoes', icon: Settings },
  ]

  const handleLogout = async () => {
    await logout()
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-white text-xl font-bold">SaaS Gestão</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-white"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
          
          <nav className="space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`nav-link ${isActive ? 'active' : ''}`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="nav-icon" />
                  {item.name}
                </Link>
              )
            })}
          </nav>
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 p-6">
          <div className="border-t border-white/20 pt-4">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">
                  {user?.username?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="ml-3">
                <p className="text-white text-sm font-medium">{user?.username}</p>
                <p className="text-white/60 text-xs">{user?.empresa}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="nav-link w-full text-left"
            >
              <LogOut className="nav-icon" />
              Sair
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="main-content flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-gray-600"
            >
              <Menu className="w-6 h-6" />
            </button>
            <div className="flex items-center space-x-4">
              <span className="text-gray-600">Bem-vindo, {user?.username}!</span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default Layout

