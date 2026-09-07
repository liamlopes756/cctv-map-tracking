FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY CctvMapTracking.sln ./
COPY src/CctvMapTracking.Api/CctvMapTracking.Api.csproj src/CctvMapTracking.Api/
RUN dotnet restore src/CctvMapTracking.Api/CctvMapTracking.Api.csproj

COPY src/CctvMapTracking.Api src/CctvMapTracking.Api
RUN dotnet publish src/CctvMapTracking.Api/CctvMapTracking.Api.csproj -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/publish .
EXPOSE 8080
ENTRYPOINT ["dotnet", "CctvMapTracking.Api.dll"]
