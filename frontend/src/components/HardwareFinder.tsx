"use client";
import React, { useState, useEffect } from "react";
import { Material } from "./CabinetBuilder";

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

  useEffect(() => {
    fetchHardware();
  }, []);

  useEffect(() => {
    // Filter hardware based on search and type
    const filtered = hardware.filter(hw => {
      const matchesSearch = hw.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (hw.description?.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesType = selectedType === "all" || hw.type === selectedType;
      return matchesSearch && matchesType;
    });
    setFilteredHardware(filtered);
  }, [searchTerm, selectedType, hardware]);

  const fetchHardware = async () => {
    try {
      setLoading(true);
      setError(null);

      // TODO: Update this URL when backend is deployed
      const response = await fetch("http://localhost:8000/api/hardware", {
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

  const hardwareTypes = Array.from(new Set(hardware.map(hw => hw.type)));
  const typeEmojis: Record<string, string> = {
    hinge: "🔩",
    slide: "📤",
    screw: "🔩",
    bracket: "🔩",
    handle: "🤲",
    knob: "⭕",
    drawer: "📦",
    door: "🚪"
  };

  if (loading) {
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
                  {typeEmojis[selectedHardware.type] || "🔩"}
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
                    Supplier: <span className="text-blue-400 ml-1">{selectedHardware.supplier}</span>
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

        <div>
          <label className="block text-slate-300 text-sm mb-2">Filter by Type</label>
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="all">All Types</option>
            {hardwareTypes.map(type => (
              <option key={type} value={type}>
                {typeEmojis[type] || "🔩"} {type.charAt(0).toUpperCase() + type.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Hardware List */}
      {filteredHardware.length === 0 ? (
        <div className="text-center py-8 text-slate-400">
          No hardware found matching your search.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {filteredHardware.map(hw => (
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
                    {typeEmojis[hw.type] || "🔩"}
                  </span>
                  <h4 className="font-semibold text-white">
                    {hw.name}
                  </h4>
                </div>
                <p className="text-lg font-bold text-green-400">
                  ${hw.price.toFixed(2)}
                </p>
              </div>

              {hw.description && (
                <p className="text-slate-400 text-sm mb-3 line-clamp-2">
                  {hw.description}
                </p>
              )}

              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400 px-2 py-1 bg-slate-700 rounded">
                  {hw.type.charAt(0).toUpperCase() + hw.type.slice(1)}
                </span>
                {hw.supplier && (
                  <span className="text-slate-400 text-xs">
                    {hw.supplier}
                  </span>
                )}
              </div>

              {hw.url && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    openSupplierLink(hw.url);
                  }}
                  className="mt-3 w-full py-2 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm"
                >
                  View Supplier
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Results Count */}
      {filteredHardware.length > 0 && (
        <p className="text-slate-400 text-sm text-center">
          Showing {filteredHardware.length} of {hardware.length} hardware items
        </p>
      )}
    </div>
  );
}