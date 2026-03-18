import { render, screen } from '@testing-library/react'
import Home from '../app/page'

// Mock Clerk
jest.mock('@clerk/nextjs', () => ({
  SignedIn: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  SignedOut: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}))

describe('Home Page', () => {
  it('renders the KerfOS brand', () => {
    render(<Home />)
    const brandElements = screen.getAllByText(/Kerf/i)
    expect(brandElements.length).toBeGreaterThan(0)
  })

  it('renders the tagline', () => {
    render(<Home />)
    expect(screen.getByText(/Precision cabinet design/i)).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<Home />)
    expect(screen.getByText(/Cabinet Builder/i)).toBeInTheDocument()
    expect(screen.getByText(/Templates/i)).toBeInTheDocument()
  })

  it('renders feature categories', () => {
    render(<Home />)
    expect(screen.getByText('Design')).toBeInTheDocument()
    expect(screen.getByText('Materials & Hardware')).toBeInTheDocument()
    expect(screen.getByText('Optimization')).toBeInTheDocument()
  })

  it('renders stats section', () => {
    render(<Home />)
    expect(screen.getByText(/Active Users/i)).toBeInTheDocument()
    expect(screen.getByText(/Cabinets Designed/i)).toBeInTheDocument()
  })

  it('renders footer with links', () => {
    render(<Home />)
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument()
    expect(screen.getByText('Terms of Service')).toBeInTheDocument()
    expect(screen.getByText('GDPR')).toBeInTheDocument()
  })
})
