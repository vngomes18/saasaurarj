import React, { useState } from 'react'
import { Settings, Save, User, Bell, Shield, Database, Palette, Globe } from 'lucide-react'

function Configuracoes() {
  const [activeTab, setActiveTab] = useState('geral')
  const [settings, setSettings] = useState({
    empresa: {
      nome: '',
      cnpj: '',
      endereco: '',
      telefone: '',
      email: ''
    },
    sistema: {
      tema: 'light',
      idioma: 'pt-BR',
      timezone: 'America/Sao_Paulo'
    },
    notificacoes: {
      email: true,
      push: false,
      sms: false
    },
    seguranca: {
      doisFatores: false,
      sessaoTimeout: 30,
      logAcesso: true
    }
  })

  const tabs = [
    {
      id: 'geral',
      name: 'Geral',
      icon: Settings,
      description: 'Configurações gerais da empresa'
    },
    {
      id: 'sistema',
      name: 'Sistema',
      icon: Database,
      description: 'Configurações do sistema'
    },
    {
      id: 'notificacoes',
      name: 'Notificações',
      icon: Bell,
      description: 'Preferências de notificação'
    },
    {
      id: 'seguranca',
      name: 'Segurança',
      icon: Shield,
      description: 'Configurações de segurança'
    },
    {
      id: 'aparencia',
      name: 'Aparência',
      icon: Palette,
      description: 'Tema e personalização'
    }
  ]

  const handleSave = () => {
    console.log('Salvando configurações:', settings)
    // Implementar salvamento das configurações
  }

  const handleInputChange = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
          <Settings className="w-8 h-8 mr-3 text-blue-600" />
          Configurações
        </h1>
        <p className="text-gray-600">Gerencie as configurações do sistema</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full text-left p-3 rounded-lg transition-all ${
                    activeTab === tab.id 
                      ? 'bg-blue-50 text-blue-700 border-l-4 border-blue-500' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center">
                    <tab.icon className="w-5 h-5 mr-3" />
                    <div>
                      <h3 className="font-medium">{tab.name}</h3>
                      <p className="text-sm text-gray-500">{tab.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          <div className="card">
            <div className="card-header">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">
                  {tabs.find(tab => tab.id === activeTab)?.name}
                </h3>
                <button 
                  className="btn btn-primary"
                  onClick={handleSave}
                >
                  <Save className="w-4 h-4 mr-2" />
                  Salvar
                </button>
              </div>
            </div>

            <div className="p-6">
              {activeTab === 'geral' && (
                <div className="space-y-6">
                  <h4 className="text-lg font-medium mb-4">Informações da Empresa</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nome da Empresa
                      </label>
                      <input
                        type="text"
                        value={settings.empresa.nome}
                        onChange={(e) => handleInputChange('empresa', 'nome', e.target.value)}
                        className="input"
                        placeholder="Digite o nome da empresa"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        CNPJ
                      </label>
                      <input
                        type="text"
                        value={settings.empresa.cnpj}
                        onChange={(e) => handleInputChange('empresa', 'cnpj', e.target.value)}
                        className="input"
                        placeholder="00.000.000/0000-00"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Telefone
                      </label>
                      <input
                        type="text"
                        value={settings.empresa.telefone}
                        onChange={(e) => handleInputChange('empresa', 'telefone', e.target.value)}
                        className="input"
                        placeholder="(00) 0000-0000"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email
                      </label>
                      <input
                        type="email"
                        value={settings.empresa.email}
                        onChange={(e) => handleInputChange('empresa', 'email', e.target.value)}
                        className="input"
                        placeholder="contato@empresa.com"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Endereço
                    </label>
                    <textarea
                      value={settings.empresa.endereco}
                      onChange={(e) => handleInputChange('empresa', 'endereco', e.target.value)}
                      className="input"
                      rows={3}
                      placeholder="Digite o endereço completo"
                    />
                  </div>
                </div>
              )}

              {activeTab === 'sistema' && (
                <div className="space-y-6">
                  <h4 className="text-lg font-medium mb-4">Configurações do Sistema</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Idioma
                      </label>
                      <select
                        value={settings.sistema.idioma}
                        onChange={(e) => handleInputChange('sistema', 'idioma', e.target.value)}
                        className="input"
                      >
                        <option value="pt-BR">Português (Brasil)</option>
                        <option value="en-US">English (US)</option>
                        <option value="es-ES">Español</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Fuso Horário
                      </label>
                      <select
                        value={settings.sistema.timezone}
                        onChange={(e) => handleInputChange('sistema', 'timezone', e.target.value)}
                        className="input"
                      >
                        <option value="America/Sao_Paulo">São Paulo (GMT-3)</option>
                        <option value="America/New_York">New York (GMT-5)</option>
                        <option value="Europe/London">London (GMT+0)</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'notificacoes' && (
                <div className="space-y-6">
                  <h4 className="text-lg font-medium mb-4">Preferências de Notificação</h4>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h5 className="font-medium">Notificações por Email</h5>
                        <p className="text-sm text-gray-600">Receber notificações importantes por email</p>
                      </div>
                      <label className="switch">
                        <input
                          type="checkbox"
                          checked={settings.notificacoes.email}
                          onChange={(e) => handleInputChange('notificacoes', 'email', e.target.checked)}
                        />
                        <span className="slider"></span>
                      </label>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h5 className="font-medium">Notificações Push</h5>
                        <p className="text-sm text-gray-600">Receber notificações no navegador</p>
                      </div>
                      <label className="switch">
                        <input
                          type="checkbox"
                          checked={settings.notificacoes.push}
                          onChange={(e) => handleInputChange('notificacoes', 'push', e.target.checked)}
                        />
                        <span className="slider"></span>
                      </label>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h5 className="font-medium">Notificações SMS</h5>
                        <p className="text-sm text-gray-600">Receber notificações por SMS</p>
                      </div>
                      <label className="switch">
                        <input
                          type="checkbox"
                          checked={settings.notificacoes.sms}
                          onChange={(e) => handleInputChange('notificacoes', 'sms', e.target.checked)}
                        />
                        <span className="slider"></span>
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'seguranca' && (
                <div className="space-y-6">
                  <h4 className="text-lg font-medium mb-4">Configurações de Segurança</h4>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h5 className="font-medium">Autenticação de Dois Fatores</h5>
                        <p className="text-sm text-gray-600">Adicionar uma camada extra de segurança</p>
                      </div>
                      <label className="switch">
                        <input
                          type="checkbox"
                          checked={settings.seguranca.doisFatores}
                          onChange={(e) => handleInputChange('seguranca', 'doisFatores', e.target.checked)}
                        />
                        <span className="slider"></span>
                      </label>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Timeout de Sessão (minutos)
                      </label>
                      <input
                        type="number"
                        value={settings.seguranca.sessaoTimeout}
                        onChange={(e) => handleInputChange('seguranca', 'sessaoTimeout', parseInt(e.target.value))}
                        className="input"
                        min="5"
                        max="120"
                      />
                    </div>
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h5 className="font-medium">Log de Acesso</h5>
                        <p className="text-sm text-gray-600">Registrar tentativas de acesso ao sistema</p>
                      </div>
                      <label className="switch">
                        <input
                          type="checkbox"
                          checked={settings.seguranca.logAcesso}
                          onChange={(e) => handleInputChange('seguranca', 'logAcesso', e.target.checked)}
                        />
                        <span className="slider"></span>
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'aparencia' && (
                <div className="space-y-6">
                  <h4 className="text-lg font-medium mb-4">Aparência e Tema</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Tema
                      </label>
                      <select
                        value={settings.sistema.tema}
                        onChange={(e) => handleInputChange('sistema', 'tema', e.target.value)}
                        className="input"
                      >
                        <option value="light">Claro</option>
                        <option value="dark">Escuro</option>
                        <option value="auto">Automático</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Configuracoes

