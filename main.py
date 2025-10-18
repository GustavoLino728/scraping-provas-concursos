from scrap import extrair_provas_banca_nivel_superior, salvar_como_csv
from filters import  filtro_interativo

def main():
    provas_superior = extrair_provas_banca_nivel_superior()
    salvar_como_csv(provas_superior)
    filtro_interativo()

if __name__ == "__main__":
    try:
        main()
    finally:
            input("\nExecução finalizada. Pressione Enter para sair...")