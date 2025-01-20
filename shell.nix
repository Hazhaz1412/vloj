let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable";
  pkgs = import nixpkgs { config = { }; overlays = [ ]; };
in

pkgs.mkShell {
  packages = with pkgs; [
    neovim
    cowsay
    lolcat
    gnumake
    libxml2
    libxslt
    zlib
    gettext
    python312Full
    python312Packages.pip
    python312Packages.mysqlclient
    python312Packages.setuptoolsBuildHook
  ];
  shellHook = ''
    cowsay "Hello, World!" | lolcat;
    export PATH="$PATH:/bin";
    export $(cat .env | xargs);
  '';
}
