import asyncio
from browser_use import Agent, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()  # legge ANTHROPIC_API_KEY dal file .env

# Configura il numero di esecuzioni desiderate
NUMERO_TEST = 1
URL_LOCALE = "http://localhost:8081"


async def esegui_singolo_test(run_id):
    print(f"\n[Test {run_id}/{NUMERO_TEST}] Avvio con Claude (Vision attivo)...")

    # Wrapper nativo di browser-use per Anthropic/Claude
    llm = ChatAnthropic(
        model="claude-sonnet-4-5",
        temperature=0.0
    )

    # Inizializziamo l'agente
    agent = Agent(
        task=f"""Visit the website at {URL_LOCALE}. 
Your task:
1. Scan the page from top to bottom to identify how it is structured.
2. Explore and find the best offers and destinations that the site offers.""",
        llm=llm,
    )

    try:
        # Avviamo l'agente
        result = await agent.run()
        # Convertiamo il risultato finale in stringa per salvarlo nel report
        return "SUCCESS", str(result)
    except Exception as e:
        return "FAILED", str(e)


async def main():
    # Creiamo o svuotiamo il file di log per questa sessione di test con Claude
    log_file_path = "risultati_test_claude.txt"
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write("=== REPORT DI TEST AUTOMATIZZATO CON CLAUDE ===\n\n")

    for i in range(1, NUMERO_TEST + 1):
        stato, report = await esegui_singolo_test(i)

        # Salviamo immediatamente il risultato nel file log
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"--- RUN {i}/{NUMERO_TEST} | STATO: {stato} ---\n")
            f.write(f"Risultato:\n{report}\n")
            f.write("-" * 50 + "\n\n")

        print(f"[Test {i}/{NUMERO_TEST}] Completato con stato: {stato}. Risultato salvato.")

        # Pausa di 3 secondi tra un test e l'altro
        await asyncio.sleep(3)

    print(f"\nTutti i {NUMERO_TEST} test sono completati! Controlla il file '{log_file_path}' per i dettagli.")


if __name__ == "__main__":
    asyncio.run(main())