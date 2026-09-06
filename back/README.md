# Backend Module

API ASP.NET Core responsavel por regras de negocio, autenticacao, persistencia e integracao com eventos do servico de IA.

## Organizacao

- `CctvMapTracking.sln`: solution .NET do modulo backend.
- `src/CctvMapTracking.Api/Program.cs`: ponto de entrada da API.
- `src/CctvMapTracking.Api/Controllers/`: controllers HTTP.
- `src/CctvMapTracking.Api/Contracts/`: DTOs e contratos de entrada/saida.
- `src/CctvMapTracking.Api/Domain/`: entidades e regras de dominio.
- `src/CctvMapTracking.Api/Infrastructure/`: persistencia, mensageria e integracoes.
- `tests/CctvMapTracking.Api.Tests/`: testes automatizados.

## Execucao

```powershell
dotnet restore
dotnet run --project src/CctvMapTracking.Api/CctvMapTracking.Api.csproj
```

API local: `http://localhost:5020`
