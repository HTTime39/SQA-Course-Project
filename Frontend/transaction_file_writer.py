class TransactionFileWriter:
  def __init__(self):
    self._fh = None
    self._filename = None

  def open_file(self, filename):
    """
    Opens the transaction output file for appending.
    """
    self._filename = filename
    # Append mode so each session/transaction adds to the same file
    self._fh = open(filename, "a", encoding="utf-8")

  def write_transaction_record(self, record_line):
    """
    Writes a single transaction record line to the output file.
    Ensures one record per line and validates the fixed length (41 chars).
    """
    if self._fh is None:
      raise RuntimeError("Transaction file is not open. Call open_file(filename) first.")

    if record_line is None:
      raise ValueError("record_line cannot be None.")

    line = str(record_line)

    # Enforce the 41-character fixed-length record format (without newline)
    # If record_line already contains a newline, strip it before checking/writing.
    line = line.rstrip("\r\n")
    if len(line) != 41:
      raise ValueError(f"Transaction record must be exactly 41 characters (got {len(line)}).")

    self._fh.write(line + "\n")
    self._fh.flush()

  def close_file(self):
    """
    Closes the output file if it's open.
    """
    if self._fh is not None:
      self._fh.close()
      self._fh = None
      self._filename = None