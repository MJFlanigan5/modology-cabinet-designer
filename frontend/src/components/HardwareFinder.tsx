"use client";
import React, { useState, useEffect } from "react";

interface Hardware {
  id: number;
  name: string;
  type: string;
  description?: string;
  price: number;
  supplier?: string;
  url?: string;
  is_active: boolean;
}

interface Supplier {
  id: string;
  name: string;
  base_url: string;
  search_url: string;
  color: string;
}

interface Category {
  id: string;
  name: string;
  icon: string;
  subtypes: string[];
}

interface HardwareFinderProps {
  selectedHardware?: Hardware | null;
  onSelect?: (hardware: Hardware) => void;
  onClear?: () => void;
}

export default function HardwareFinder({
  selectedHardware,
  onSelect,
  onClear
}: HardwareFinderProps) {
  const [loading, setLoading] = useState(false);
  const [hardware, setHardware] = useState<Hardware[]>([]);
  const [filteredHardware, setFilteredHardware] = useState<Hardware[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedType, setSelectedType] = useState<string>("all");
  const [selectedSupplier, setSelectedSupplier] = useState<string>("all");
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [categories, setCategories] = useState<Record<string, Category>>({});
  const [showSupplierSearch, setShowSupplierSearch] = useState(false);
  const [supplierSearchResults, setSupplierSearchResults] = useState<Supplier[]>([]);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    fetchSuppliers();
    fetchCategories();
    fetchHardware();
  }, []);

  useEffect(() => {
    // Filter hardware based on search, type, and supplier
    const filtered = hardware.filter(hw => {
      const matchesSearch = hw.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (hw.description?.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesType = selectedType === "all" || hw.type === selectedType;
      const matchesSupplier = selectedSupplier === "all" || hw.supplier === selectedSupplier;
      return matchesSearch && matchesType && matchesSupplier;
    });
    setFilteredHardware(filtered);
  }, [searchTerm, selectedType, selectedSupplier, hardware]);

  const fetchSuppliers = async () => {
    try {
      const response = await fetch(`${API_URL}/api/hardware/suppliers`);
      if (response.ok) {
        const data: Supplier[] = await response.json();
        setSuppliers(data);
      }
    } catch (err) {
      console.error("Failed to fetch suppliers:", err);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_URL}/api/hardware/categories`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (err) {
      console.error("Failed to fetch categories:", err);
    }
  };

  const fetchHardware = async () => {
    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      if (selectedType !== "all") params.append("type", selectedType);
      if (selectedSupplier !== "all") params.append("supplier", selectedSupplier);
      if (searchTerm) params.append("search", searchTerm);

      const response = await fetch(`${API_URL}/api/hardware?${params.toString()}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) {
        throw new Error("Failed to fetch hardware");
      }

      const data: Hardware[] = await response.json();
      setHardware(data);
    } catch (err) {
      setError("Could not load hardware. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const searchSuppliers = async (query: string) => {
    if (!query.trim()) {
      setSupplierSearchResults([]);
      return;
    }
    
    try {
      const response = await fetch(`${API_URL}/api/hardware/search/${encodeURIComponent(query)}`);
      if (response.ok) {
        const data = await response.json();
        setSupplierSearchResults(data);
      }
    } catch (err) {
      console.error("Failed to search suppliers:", err);
    }
  };

  const seedDatabase = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/hardware/seed`, {
        method: "POST"
      });
      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        fetchHardware();
      }
    } catch (err) {
      console.error("Failed to seed hardware:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (hw: Hardware) => {
    if (onSelect) {
      onSelect(hw);
    }
  };

  const handleClear = () => {
    if (onClear) {
      onClear();
    }
  };

  const openSupplierLink = (url?: string) => {
    if (url) {
      window.open(url, "_blank");
    }
  };

  const getSupplierInfo = (supplierId?: string): Supplier | undefined => {
    if (!supplierId) return undefined;
    return suppliers.find(s => s.id === supplierId);
  };

  const getTypeEmoji = (type: string): string => {
    return categories[type]?.icon || "🔩";
  };

  const hardwareTypes = Array.from(new Set(hardware.map(hw => hw.type)));

  if (loading && hardware.length === 0) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin text-4xl mr-3">⚙️</div>
        <p className="text-slate-400">Loading hardware...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-700 p-4 rounded-lg">
        <p className="text-red-300 text-sm">{error}</p>
        <button
          onClick={fetchHardware}
          className="mt-2 px-4 py-2 bg-red-700 hover:bg-red-600 text-white rounded text-sm"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Selected Hardware Display */}
      {selectedHardware && (
        <div className="bg-blue-900/20 border border-blue-700 p-4 rounded-lg">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center mb-2">
                <span className="text-2xl mr-2">
                  {getTypeEmoji(selectedHardware.type)}
                </span>
                <h3 className="font-semibold text-white text-lg">
                  {selectedHardware.name}
                </h3>
              </div>
              <p className="text-slate-400 text-sm mb-2">
                {selectedHardware.description || "No description"}
              </p>
              <div className="flex items-center space-x-4 text-sm">
                <span className="text-slate-300">
                  Type: <span className="text-blue-400 ml-1">{selectedHardware.type}</span>
                </span>
                {selectedHardware.supplier && (
                  <span className="text-slate-300">
                    Supplier: 
                    <span 
                      className="ml-1 px-2 py-0.5 rounded text-xs"
                      style={{ 
                        backgroundColor: getSupplierInfo(selectedHardware.supplier)?.color + "40",
                        color: getSupplierInfo(selectedHardware.supplier)?.color
                      }}
                    >
                      {getSupplierInfo(selectedHardware.supplier)?.name || selectedHardware.supplier}
                    </span>
                  </span>
                )}
              </div>
            </div>
            <div className="ml-4 flex flex-col items-end space-y-2">
              <p className="text-2xl font-bold text-green-400">
                ${selectedHardware.price.toFixed(2)}
              </p>
              <button
                onClick={handleClear}
                className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm"
              >
                Clear
              </button>
              {selectedHardware.url && (
                <button
                  onClick={() => openSupplierLink(selectedHardware.url)}
                  className="px-3 py-1 bg-blue-700 hover:bg-blue-600 text-white rounded text-sm"
                >
                  View Supplier
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Supplier Search Toggle */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setShowSupplierSearch(!showSupplierSearch)}
          className="text-sm text-blue-400 hover:text-blue-300 flex items-center"
        >
          🔗 {showSupplierSearch ? "Hide" : "Show"} Supplier Search
        </button>
        <button
          onClick={seedDatabase}
          className="text-sm text-green-400 hover:text-green-300"
        >
          📦 Seed Sample Data
        </button>
      </div>

      {/* Supplier Search Panel */}
      {showSupplierSearch && (
        <div className="bg-slate-800/50 border border-slate-700 p-4 rounded-lg space-y-3">
          <h4 className="text-white font-medium">Search All Suppliers</h4>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Search across all suppliers..."
              className="flex-1 px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
              onChange={(e) => searchSuppliers(e.target.value)}
            />
          </div>
          {supplierSearchResults.length > 0 && (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {supplierSearchResults.map((supplier) => (
                <button
                  key={supplier.id}
                  onClick={() => openSupplierLink(supplier.search_url)}
                  className="p-3 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors"
                  style={{ borderLeftColor: supplier.color, borderLeftWidth: 3 }}
                >
                  <div className="text-white font-medium text-sm">{supplier.name}</div>
                  <div className="text-slate-400 text-xs">Open search →</div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Search and Filter */}
      <div className="space-y-3">
        <div>
          <label className="block text-slate-300 text-sm mb-2">Search Hardware</label>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by name or description..."
            className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-slate-300 text-sm mb-2">Filter by Type</label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="all">All Types</option>
              {Object.entries(categories).map(([key, cat]) => (
                <option key={key} value={key}>
                  {cat.icon} {cat.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-slate-300 text-sm mb-2">Filter by Supplier</label>
            <select
              value={selectedSupplier}
              onChange={(e) => setSelectedSupplier(e.target.value)}
              className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="all">All Suppliers</option>
              {suppliers.map((supplier) => (
                <option key={supplier.id} value={supplier.id}>
                  {supplier.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Hardware List */}
      {filteredHardware.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          <p>No hardware found matching your search.</p>
          <p className="text-sm mt-2">Try seeding sample data or adjusting filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {filteredHardware.map(hw => {
            const supplierInfo = getSupplierInfo(hw.supplier);
            const categoryInfo = categories[hw.type];
            
            return (
              <div
                key={hw.id}
                onClick={() => handleSelect(hw)}
                className={`
                  bg-slate-800 border-2 rounded-lg p-4 cursor-pointer transition-all
                  hover:shadow-lg hover:border-blue-500
                  ${selectedHardware?.id === hw.id
                    ? "border-blue-500 shadow-lg shadow-blue-500/20"
                    : "border-slate-700"
                  }
                `}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center flex-1">
                    <span className="text-2xl mr-2">
                      {categoryInfo?.icon || "🔩"}
                    </span>
                    <h4 className="font-semibold text-white text-sm">
                      {hw.name}
                    </h4>
                  </div>
                  <p className="text-lg font-bold text-green-400">
                    ${hw.price.toFixed(2)}
                  </p>
                </div>

                {hw.description && (
                  <p className="text-slate-400 text-xs mb-3 line-clamp-2">
                    {hw.description}
                  </p>
                )}

                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400 px-2 py-1 bg-slate-700 rounded">
                    {categoryInfo?.name || hw.type}
                  </span>
                  {supplierInfo && (
                    <span 
                      className="px-2 py-1 rounded text-xs"
                      style={{ 
                        backgroundColor: supplierInfo.color + "30",
                        color: supplierInfo.color
                      }}
                    >
                      {supplierInfo.name}
                    </span>
                  )}
                </div>

                {hw.url && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      openSupplierLink(hw.url);
                    }}
                    className="mt-3 w-full py-2 bg-slate-700 hover:bg-slate-600 text-white rounded text-xs"
                  >
                    View Supplier
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Results Count */}
      {filteredHardware.length > 0 && (
        <p className="text-slate-400 text-sm text-center">
          Showing {filteredHardware.length} of {hardware.length} hardware items
        </p>
      )}

      {/* Supplier Legend */}
      <div className="border-t border-slate-700 pt-4">
        <h4 className="text-slate-300 text-sm font-medium mb-2">Supported Suppliers</h4>
        <div className="flex flex-wrap gap-2">
          {suppliers.map((supplier) => (
            <button
              key={supplier.id}
              onClick={() => openSupplierLink(supplier.base_url)}
              className="px-3 py-1 rounded-full text-xs text-white hover:opacity-80 transition-opacity"
              style={{ backgroundColor: supplier.color }}
            >
              {supplier.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
