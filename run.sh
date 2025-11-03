#!/bin/bash
################################################################################
# Script de Execução do Sistema de Detecção de Gado
################################################################################
# 
# Este script facilita a execução do projeto, oferecendo diferentes opções:
# 1. Executar com Docker (recomendado)
# 2. Executar localmente
# 3. Construir imagem Docker
# 4. Limpar outputs
#
################################################################################

set -e  # Para execução em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   🐄 Sistema de Detecção e Contagem de Gado - YOLOv8   ║"
    echo "║              Script de Execução                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Função para verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker não está instalado!${NC}"
        echo "Instale o Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}⚠️  docker-compose não encontrado. Tentando usar 'docker compose'...${NC}"
        DOCKER_COMPOSE_CMD="docker compose"
    else
        DOCKER_COMPOSE_CMD="docker-compose"
    fi
}

# Função para verificar se Python está instalado
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 não está instalado!${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} encontrado${NC}"
}

# Função para construir imagem Docker
build_docker() {
    echo -e "${BLUE}🔨 Construindo imagem Docker...${NC}"
    check_docker
    $DOCKER_COMPOSE_CMD build
    echo -e "${GREEN}✅ Imagem construída com sucesso!${NC}"
}

# Função para executar com Docker
run_docker() {
    echo -e "${BLUE}🐳 Executando com Docker...${NC}"
    check_docker
    
    # Verifica se a imagem existe, senão constrói
    if ! docker images | grep -q "cattle-detector"; then
        echo -e "${YELLOW}⚠️  Imagem não encontrada. Construindo...${NC}"
        build_docker
    fi
    
    # Cria diretório de output se não existir
    mkdir -p output
    
    # Executa o container
    $DOCKER_COMPOSE_CMD up
    
    echo -e "${GREEN}✅ Processamento concluído!${NC}"
    echo -e "${BLUE}📁 Resultados salvos em: ./output/${NC}"
}

# Função para executar localmente
run_local() {
    echo -e "${BLUE}💻 Executando localmente...${NC}"
    check_python
    
    # Verifica se o ambiente virtual existe
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado. Criando...${NC}"
        python3 -m venv venv
    fi
    
    # Ativa o ambiente virtual
    echo -e "${BLUE}📦 Ativando ambiente virtual...${NC}"
    source venv/bin/activate
    
    # Instala/atualiza dependências
    echo -e "${BLUE}📥 Instalando dependências...${NC}"
    pip install --upgrade pip > /dev/null
    pip install -r requirements.txt
    
    # Cria diretório de output se não existir
    mkdir -p output
    
    # Executa o script
    echo -e "${BLUE}🚀 Iniciando detecção...${NC}"
    python detect_cattle.py
    
    echo -e "${GREEN}✅ Processamento concluído!${NC}"
    echo -e "${BLUE}📁 Resultados salvos em: ./output/${NC}"
    
    # Desativa o ambiente virtual
    deactivate
}

# Função para limpar outputs
clean() {
    echo -e "${YELLOW}🧹 Limpando diretório de saída...${NC}"
    
    if [ -d "output" ]; then
        rm -rf output/*
        echo -e "${GREEN}✅ Diretório output limpo!${NC}"
    else
        echo -e "${BLUE}ℹ️  Diretório output não existe.${NC}"
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "Uso: ./run.sh [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  docker         Executa usando Docker (recomendado)"
    echo "  local          Executa localmente sem Docker"
    echo "  build          Constrói a imagem Docker"
    echo "  clean          Limpa o diretório de saída"
    echo "  help           Mostra esta mensagem de ajuda"
    echo ""
    echo "Exemplos:"
    echo "  ./run.sh docker       # Executa com Docker"
    echo "  ./run.sh local        # Executa localmente"
    echo "  ./run.sh build        # Apenas constrói a imagem"
    echo "  ./run.sh clean        # Limpa outputs"
    echo ""
}

# Menu interativo
interactive_menu() {
    print_banner
    echo "Escolha uma opção:"
    echo ""
    echo "  1) 🐳 Executar com Docker (recomendado)"
    echo "  2) 💻 Executar localmente"
    echo "  3) 🔨 Construir imagem Docker"
    echo "  4) 🧹 Limpar outputs"
    echo "  5) ❌ Sair"
    echo ""
    read -p "Digite o número da opção: " choice
    
    case $choice in
        1)
            run_docker
            ;;
        2)
            run_local
            ;;
        3)
            build_docker
            ;;
        4)
            clean
            ;;
        5)
            echo -e "${BLUE}👋 Até logo!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção inválida!${NC}"
            exit 1
            ;;
    esac
}

# Main
main() {
    # Se não há argumentos, mostra menu interativo
    if [ $# -eq 0 ]; then
        interactive_menu
        exit 0
    fi
    
    # Processa argumentos
    case "$1" in
        docker)
            print_banner
            run_docker
            ;;
        local)
            print_banner
            run_local
            ;;
        build)
            print_banner
            build_docker
            ;;
        clean)
            print_banner
            clean
            ;;
        help|--help|-h)
            print_banner
            show_help
            ;;
        *)
            echo -e "${RED}❌ Opção inválida: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Executa o script
main "$@"
