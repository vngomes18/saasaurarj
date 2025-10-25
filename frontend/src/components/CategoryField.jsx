import React, { useState, useEffect, useRef } from 'react'
import { ChevronDown, Plus, Search } from 'lucide-react'
import { useCategories } from '../hooks/useApi'
import CategoryModal from './CategoryModal'

function CategoryField({ value, onChange, placeholder = "Selecione uma categoria" }) {
  const [isOpen, setIsOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const dropdownRef = useRef(null)
  const inputRef = useRef(null)

  const { data: categories = [], isLoading } = useCategories()

  // Filtrar categorias baseado no termo de busca
  const filteredCategories = categories.filter(category =>
    category.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Fechar dropdown quando clicar fora
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
        setSearchTerm('')
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Atualizar valor quando categoria for selecionada
  const handleCategorySelect = (category) => {
    onChange(category)
    setIsOpen(false)
    setSearchTerm('')
  }

  // Abrir modal para nova categoria
  const handleCreateCategory = () => {
    setShowModal(true)
    setIsOpen(false)
  }

  // Callback quando nova categoria for criada
  const handleCategoryCreated = (newCategory) => {
    onChange(newCategory)
    setShowModal(false)
  }

  // Focar no input quando dropdown abrir
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Campo de entrada */}
      <div
        className="relative cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
      >
        <input
          ref={inputRef}
          type="text"
          value={value || ''}
          onChange={(e) => {
            setSearchTerm(e.target.value)
            if (!isOpen) setIsOpen(true)
          }}
          onFocus={() => setIsOpen(true)}
          placeholder={placeholder}
          className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          readOnly={!isOpen}
        />
        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </div>
      </div>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {/* Campo de busca */}
          <div className="p-2 border-b border-gray-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar categorias..."
                className="w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
              />
            </div>
          </div>

          {/* Lista de categorias */}
          <div className="py-1">
            {isLoading ? (
              <div className="px-3 py-2 text-sm text-gray-500 text-center">
                Carregando categorias...
              </div>
            ) : filteredCategories.length > 0 ? (
              filteredCategories.map((category, index) => (
                <button
                  key={index}
                  onClick={() => handleCategorySelect(category)}
                  className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 focus:bg-gray-100 focus:outline-none"
                >
                  {category}
                </button>
              ))
            ) : (
              <div className="px-3 py-2 text-sm text-gray-500">
                {searchTerm ? 'Nenhuma categoria encontrada' : 'Nenhuma categoria cadastrada'}
              </div>
            )}

            {/* Botão para criar nova categoria */}
            <button
              onClick={handleCreateCategory}
              className="w-full px-3 py-2 text-left text-sm text-blue-600 hover:bg-blue-50 focus:bg-blue-50 focus:outline-none flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Criar nova categoria
            </button>
          </div>
        </div>
      )}

      {/* Modal para criar categoria */}
      <CategoryModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onCategoryCreated={handleCategoryCreated}
        existingCategories={categories}
      />
    </div>
  )
}

export default CategoryField
