'use client';

import React, { useState, useEffect } from 'react';

interface CommunityGalleryProps {
  onSelectProject?: (project: GalleryProject) => void;
}

interface GalleryProject {
  id: string;
  name: string;
  author: string;
  authorAvatar?: string;
  description: string;
  images: string[];
  cabinetType: string;
  style: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedCost: number;
  actualCost?: number;
  buildTime: number; // hours
  rating: number;
  reviewCount: number;
  tags: string[];
  tips: string[];
  materials: string[];
  createdAt: Date;
  featured: boolean;
}

const CommunityGallery: React.FC<CommunityGalleryProps> = ({ onSelectProject }) => {
  const [projects, setProjects] = useState<GalleryProject[]>([]);
  const [filteredProjects, setFilteredProjects] = useState<GalleryProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedProject, setSelectedProject] = useState<GalleryProject | null>(null);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStyle, setSelectedStyle] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [selectedCabinetType, setSelectedCabinetType] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'popular' | 'recent' | 'cost'>('popular');

  const styles = ['all', 'shaker', 'flat-panel', 'raised-panel', 'slab', 'rustic', 'modern', 'traditional'];
  const difficulties = ['all', 'beginner', 'intermediate', 'advanced'];
  const cabinetTypes = ['all', 'kitchen', 'bathroom', 'garage', 'office', 'living-room', 'bedroom'];

  useEffect(() => {
    // Simulate API fetch
    const fetchProjects = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockProjects: GalleryProject[] = [
        {
          id: '1',
          name: 'Modern Farmhouse Kitchen',
          author: 'WoodWorkerMike',
          description: 'Complete kitchen renovation with shaker-style cabinets, soft-close drawers, and a massive center island. Used pre-finished maple plywood with maple face frames.',
          images: ['/projects/kitchen1.jpg', '/projects/kitchen1-2.jpg'],
          cabinetType: 'kitchen',
          style: 'shaker',
          difficulty: 'intermediate',
          estimatedCost: 4500,
          actualCost: 4200,
          buildTime: 120,
          rating: 4.8,
          reviewCount: 45,
          tags: ['kitchen', 'island', 'soft-close', 'maple'],
          tips: [
            'Pre-finished plywood saves tons of time on finishing',
            'Use a story pole for consistent measurements',
            'Label every part as you cut',
          ],
          materials: ['3/4" Maple Plywood', '1x4 Maple (face frames)', 'Blum soft-close slides', 'Concealed hinges'],
          createdAt: new Date('2024-01-15'),
          featured: true,
        },
        {
          id: '2',
          name: 'Garage Storage System',
          author: 'DIYDan',
          description: 'Full-wall storage with cabinets, workbench, and overhead compartments. Built from birch plywood with melamine countertops.',
          images: ['/projects/garage1.jpg'],
          cabinetType: 'garage',
          style: 'flat-panel',
          difficulty: 'beginner',
          estimatedCost: 1200,
          actualCost: 1350,
          buildTime: 40,
          rating: 4.5,
          reviewCount: 28,
          tags: ['garage', 'storage', 'workbench', 'budget-friendly'],
          tips: [
            'Use 3/4" plywood for durability',
            'Add adjustable shelf pins for flexibility',
            'Include toe kick space for comfort',
          ],
          materials: ['3/4" Birch Plywood', 'Melamine sheets', 'Heavy-duty shelf pins'],
          createdAt: new Date('2024-02-20'),
          featured: false,
        },
        {
          id: '3',
          name: 'Floating Bathroom Vanity',
          author: 'ModernMaker',
          description: 'Wall-mounted double vanity with vessel sinks. Walnut veneer with LED under-cabinet lighting.',
          images: ['/projects/vanity1.jpg', '/projects/vanity1-2.jpg'],
          cabinetType: 'bathroom',
          style: 'modern',
          difficulty: 'advanced',
          estimatedCost: 1800,
          actualCost: 2100,
          buildTime: 65,
          rating: 4.9,
          reviewCount: 32,
          tags: ['bathroom', 'floating', 'modern', 'walnut'],
          tips: [
            'Use a French cleat for secure wall mounting',
            'Seal all surfaces for bathroom moisture',
            'Plan plumbing access carefully',
          ],
          materials: ['Walnut veneer plywood', 'Solid walnut edge banding', 'LED strip lights'],
          createdAt: new Date('2024-03-01'),
          featured: true,
        },
        {
          id: '4',
          name: 'Built-In Bookshelves',
          author: 'ClassicCarpenter',
          description: 'Floor-to-ceiling built-in bookcases with integrated desk. Paint-grade with adjustable shelves.',
          images: ['/projects/bookshelf1.jpg'],
          cabinetType: 'living-room',
          style: 'traditional',
          difficulty: 'intermediate',
          estimatedCost: 900,
          buildTime: 35,
          rating: 4.6,
          reviewCount: 19,
          tags: ['bookshelf', 'built-in', 'desk', 'living-room'],
          tips: [
            'Scribe to wall for seamless fit',
            'Use pocket holes for invisible joinery',
            'Crown molding adds a professional touch',
          ],
          materials: ['MDF', 'Poplar (face frames)', 'Crown molding'],
          createdAt: new Date('2024-02-05'),
          featured: false,
        },
        {
          id: '5',
          name: 'Kids Playroom Storage',
          author: 'FamilyBuilder',
          description: 'Colorful cubby storage system with bins and hooks. Rounded corners for safety.',
          images: ['/projects/playroom1.jpg'],
          cabinetType: 'bedroom',
          style: 'slab',
          difficulty: 'beginner',
          estimatedCost: 500,
          actualCost: 480,
          buildTime: 20,
          rating: 4.4,
          reviewCount: 15,
          tags: ['kids', 'storage', 'cubbies', 'beginner'],
          tips: [
            'Round all corners for child safety',
            'Use durable, washable paint',
            'Include label holders for organization',
          ],
          materials: ['Birch plywood', 'Fabric bins', 'Plastic label holders'],
          createdAt: new Date('2024-03-10'),
          featured: false,
        },
        {
          id: '6',
          name: 'Rustic Pantry Cabinet',
          author: 'BarnwoodBob',
          description: 'Freestanding pantry with distressed finish. Reclaimed barn wood accents and chicken wire door panels.',
          images: ['/projects/pantry1.jpg', '/projects/pantry1-2.jpg'],
          cabinetType: 'kitchen',
          style: 'rustic',
          difficulty: 'intermediate',
          estimatedCost: 800,
          buildTime: 45,
          rating: 4.7,
          reviewCount: 22,
          tags: ['pantry', 'rustic', 'reclaimed', 'freestanding'],
          tips: [
            'Distress before final finish',
            'Use gel stain for even color on pine',
            'Seal interior for easy cleaning',
          ],
          materials: ['Pine plywood', 'Reclaimed barn wood', 'Chicken wire'],
          createdAt: new Date('2024-01-28'),
          featured: true,
        },
      ];

      setProjects(mockProjects);
      setFilteredProjects(mockProjects);
      setLoading(false);
    };

    fetchProjects();
  }, []);

  useEffect(() => {
    let filtered = [...projects];

    // Apply filters
    if (searchQuery) {
      filtered = filtered.filter(p => 
        p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    if (selectedStyle !== 'all') {
      filtered = filtered.filter(p => p.style === selectedStyle);
    }

    if (selectedDifficulty !== 'all') {
      filtered = filtered.filter(p => p.difficulty === selectedDifficulty);
    }

    if (selectedCabinetType !== 'all') {
      filtered = filtered.filter(p => p.cabinetType === selectedCabinetType);
    }

    // Apply sort
    switch (sortBy) {
      case 'popular':
        filtered.sort((a, b) => b.rating * b.reviewCount - a.rating * a.reviewCount);
        break;
      case 'recent':
        filtered.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
        break;
      case 'cost':
        filtered.sort((a, b) => a.estimatedCost - b.estimatedCost);
        break;
    }

    setFilteredProjects(filtered);
  }, [searchQuery, selectedStyle, selectedDifficulty, selectedCabinetType, sortBy, projects]);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderStars = (rating: number) => {
    return '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
  };

  if (selectedProject) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <button
          onClick={() => setSelectedProject(null)}
          className="mb-4 text-blue-600 hover:text-blue-800 flex items-center gap-1"
        >
          ← Back to Gallery
        </button>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Images */}
          <div>
            <div className="bg-gray-200 rounded-lg h-80 flex items-center justify-center">
              <span className="text-gray-500">📷 Project Images</span>
            </div>
            <div className="flex gap-2 mt-2">
              {selectedProject.images.map((_, i) => (
                <div key={i} className="w-16 h-16 bg-gray-200 rounded cursor-pointer hover:opacity-80" />
              ))}
            </div>
          </div>

          {/* Details */}
          <div>
            <div className="flex items-start justify-between mb-2">
              <h2 className="text-2xl font-bold">{selectedProject.name}</h2>
              {selectedProject.featured && (
                <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm font-medium">
                  ⭐ Featured
                </span>
              )}
            </div>

            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gray-300 rounded-full" />
              <span className="font-medium">{selectedProject.author}</span>
            </div>

            <p className="text-gray-600 mb-4">{selectedProject.description}</p>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-500">Estimated Cost</p>
                <p className="text-xl font-bold">${selectedProject.estimatedCost}</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-500">Build Time</p>
                <p className="text-xl font-bold">{selectedProject.buildTime} hrs</p>
              </div>
            </div>

            <div className="flex gap-2 mb-4">
              <span className={`px-2 py-1 rounded text-sm ${getDifficultyColor(selectedProject.difficulty)}`}>
                {selectedProject.difficulty}
              </span>
              <span className="px-2 py-1 rounded text-sm bg-blue-100 text-blue-800 capitalize">
                {selectedProject.style}
              </span>
            </div>

            <div className="flex items-center gap-1 text-yellow-500 mb-4">
              <span>{renderStars(selectedProject.rating)}</span>
              <span className="text-gray-500 text-sm ml-1">
                ({selectedProject.reviewCount} reviews)
              </span>
            </div>

            <div className="flex flex-wrap gap-2 mb-4">
              {selectedProject.tags.map((tag) => (
                <span key={tag} className="px-2 py-1 bg-gray-100 rounded text-sm text-gray-600">
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Tips */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-3">💡 Tips from {selectedProject.author}</h3>
          <ul className="space-y-2">
            {selectedProject.tips.map((tip, i) => (
              <li key={i} className="flex gap-2 text-gray-600">
                <span className="text-green-500">✓</span>
                {tip}
              </li>
            ))}
          </ul>
        </div>

        {/* Materials */}
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-3">📦 Materials Used</h3>
          <div className="flex flex-wrap gap-2">
            {selectedProject.materials.map((material) => (
              <span key={material} className="px-3 py-1 border rounded-full text-sm">
                {material}
              </span>
            ))}
          </div>
        </div>

        <button
          onClick={() => onSelectProject?.(selectedProject)}
          className="mt-6 w-full py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600"
        >
          Use This Design as Template
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <span className="text-3xl">🏠</span>
        Community Build Gallery
      </h2>

      <p className="text-gray-600 mb-6">
        Browse designs others have actually built. Learn from real experiences.
      </p>

      {/* Filters */}
      <div className="space-y-4 mb-6">
        {/* Search */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search projects, tags, or styles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="text-sm text-gray-500 block mb-1">Style</label>
            <select
              value={selectedStyle}
              onChange={(e) => setSelectedStyle(e.target.value)}
              className="border rounded px-3 py-1.5 text-sm"
            >
              {styles.map((s) => (
                <option key={s} value={s}>{s === 'all' ? 'All Styles' : s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-500 block mb-1">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="border rounded px-3 py-1.5 text-sm"
            >
              {difficulties.map((d) => (
                <option key={d} value={d}>{d === 'all' ? 'All Levels' : d}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-500 block mb-1">Room</label>
            <select
              value={selectedCabinetType}
              onChange={(e) => setSelectedCabinetType(e.target.value)}
              className="border rounded px-3 py-1.5 text-sm"
            >
              {cabinetTypes.map((t) => (
                <option key={t} value={t}>{t === 'all' ? 'All Rooms' : t}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-500 block mb-1">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="border rounded px-3 py-1.5 text-sm"
            >
              <option value="popular">Most Popular</option>
              <option value="recent">Most Recent</option>
              <option value="cost">Lowest Cost</option>
            </select>
          </div>
        </div>
      </div>

      {/* Projects Grid */}
      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading projects...</p>
        </div>
      ) : filteredProjects.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No projects match your filters.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredProjects.map((project) => (
            <div
              key={project.id}
              onClick={() => setSelectedProject(project)}
              className="border rounded-lg overflow-hidden cursor-pointer hover:shadow-lg transition"
            >
              <div className="h-40 bg-gray-200 flex items-center justify-center">
                {project.featured && (
                  <span className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-2 py-0.5 rounded text-xs font-medium">
                    Featured
                  </span>
                )}
                <span className="text-gray-400">📷</span>
              </div>

              <div className="p-4">
                <h3 className="font-semibold mb-1">{project.name}</h3>
                <p className="text-sm text-gray-500 mb-2">by {project.author}</p>

                <div className="flex items-center gap-1 text-yellow-500 text-sm mb-2">
                  <span>{renderStars(project.rating)}</span>
                  <span className="text-gray-400">({project.reviewCount})</span>
                </div>

                <div className="flex justify-between items-center text-sm">
                  <span className={`px-2 py-0.5 rounded ${getDifficultyColor(project.difficulty)}`}>
                    {project.difficulty}
                  </span>
                  <span className="font-semibold">${project.estimatedCost}</span>
                </div>

                <div className="flex flex-wrap gap-1 mt-2">
                  {project.tags.slice(0, 3).map((tag) => (
                    <span key={tag} className="text-xs text-gray-500">#{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CommunityGallery;
