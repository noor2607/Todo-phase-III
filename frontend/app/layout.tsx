import './globals.css';
import { Inter } from 'next/font/google';
import { AuthProvider } from '../providers/AuthProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Todo App',
  description: 'A simple todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div id="modal-root" />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}