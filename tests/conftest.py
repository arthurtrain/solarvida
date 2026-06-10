import sys, os
# coloca backend/ no path para os imports do projeto funcionarem nos testes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
