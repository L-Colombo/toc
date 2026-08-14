{
  description = "A CLI utility to add table of contents to PDFs";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        strictDeps = true;

        nativeBuildInputs = with pkgs; [
          python313
          uv

          # deps
          python313Packages.click
          python313Packages.chardet
          python313Packages.pymupdf
        ];

        buildInputs = with pkgs; [
          libclang
          stdenv.cc.cc.lib
        ];

        shellHook = ''
          export PS1="(dev) $PS1"
          source .venv/bin/activate
          uv pip install --editable .
        '';

        LIBCLANG_PATH = with pkgs; "${libclang.lib}/lib";
        LD_LIBRARY_PATH = with pkgs; "${stdenv.cc.cc.lib}/lib";
      };
    };
}
