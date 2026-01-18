import { useState } from 'react';

interface FilterOptions {
  status: 'all' | 'pending' | 'completed';
  sortBy: 'created_at' | 'title';
  sortOrder: 'asc' | 'desc';
}

interface FiltersProps {
  onFilterChange: (filters: FilterOptions) => void;
}

const Filters = ({ onFilterChange }: FiltersProps) => {
  const [filters, setFilters] = useState<FilterOptions>({
    status: 'all',
    sortBy: 'created_at',
    sortOrder: 'desc'
  });

  const handleStatusChange = (status: 'all' | 'pending' | 'completed') => {
    const newFilters = { ...filters, status };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleSortChange = (sortBy: 'created_at' | 'title', order: 'asc' | 'desc') => {
    const newFilters = { ...filters, sortBy, sortOrder: order };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white shadow rounded-lg p-4 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Status Filter */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Status</h3>
          <div className="flex space-x-2">
            {(['all', 'pending', 'completed'] as const).map(status => (
              <button
                key={status}
                onClick={() => handleStatusChange(status)}
                className={`px-3 py-1 text-sm rounded-full ${
                  filters.status === status
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Sort By */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Sort By</h3>
          <div className="flex space-x-2">
            <button
              onClick={() => handleSortChange('created_at', filters.sortOrder === 'asc' ? 'desc' : 'asc')}
              className={`px-3 py-1 text-sm rounded ${
                filters.sortBy === 'created_at'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Created {filters.sortBy === 'created_at' && (filters.sortOrder === 'asc' ? '↑' : '↓')}
            </button>
            <button
              onClick={() => handleSortChange('title', filters.sortOrder === 'asc' ? 'desc' : 'asc')}
              className={`px-3 py-1 text-sm rounded ${
                filters.sortBy === 'title'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Title {filters.sortBy === 'title' && (filters.sortOrder === 'asc' ? '↑' : '↓')}
            </button>
          </div>
        </div>

        {/* Sort Direction */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Order</h3>
          <div className="flex space-x-2">
            <button
              onClick={() => handleSortChange(filters.sortBy, 'asc')}
              className={`px-3 py-1 text-sm rounded ${
                filters.sortOrder === 'asc'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Ascending
            </button>
            <button
              onClick={() => handleSortChange(filters.sortBy, 'desc')}
              className={`px-3 py-1 text-sm rounded ${
                filters.sortOrder === 'desc'
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Descending
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Filters;